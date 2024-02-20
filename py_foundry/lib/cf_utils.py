import json
import os
from typing import Callable, Optional

from lib.log_config import cf_logger
from lib.methods import run_command
from lib.service_integration import CloudFoundryService


class ServiceKey(CloudFoundryService):
        
    def __init__(self,
                 service_name: str,
                 service_key_name: str = 'SharedDevKey',
                 call_cf: Callable[[str, bool], str] = run_command
                 ) -> None:
        super().__init__(call_cf)

        self.service_name = service_name
        self.service_key_name = service_key_name

    def fetch_service_key(self) -> dict:
        service_key_text = self.service_key(self.service_name, self.service_key_name)
        return json.loads(service_key_text)

    def fetch_service_key_credentials(self) -> dict:
        service_key = self.fetch_service_key()
        return service_key.get('credentials')

    def create(self,
               service_name: str,
               service_key_name: str,
               json_params: Optional[str],  # Not sure why when calling this method, json_params is mandatory
               wait: bool = True) -> str:
        return self.create_service_key(service_name, service_key_name, json_params=json_params, wait=wait)

    def delete(self,
               service_name: str,
               service_key_name: str,
               force: bool = False,
               wait: bool = True) -> str:
        return self.delete_service_key(service_name, service_key_name, force, wait)

class CreateService:
    def __init__(self,
                 service_name: str,
                 service_type: Optional[str],
                 service_plan: Optional[str],
                 json_params: Optional[str],
                 call_cf: Callable[[str, bool], str] = run_command
                 ) -> None:
        self.service_name = service_name
        self.service_type = service_type
        self.service_plan = service_plan
        self.json_params = json_params
        self._call_cf = call_cf

    def create_service_command(self) -> str:
        cf_logger.info(f'Creating service {self.service_name}')

        c = f"cf create-service {self.service_type} {self.service_plan} {self.service_name}"

        if self.json_params is not None:
            c = ' '.join([c, f"-c '{self.json_params}'"])

        self._call_cf


class CreateUserProvidedService:
    def __init__(self,
                 service_name: str,
                 json_params: Optional[str],
                 call_cf: Callable[[str, bool], str] = run_command
                 ) -> None:
        self.service_name = service_name
        self.json_params = json_params
        self._call_cf = call_cf

    def create_service_command(self) -> str:
        cf_logger.info(f'Creating service {self.service_name}')

        c = f"cf create-user-provided-service {self.service_name}"

        if self.json_params is not None:
            c = ' '.join([c, f"-c '{self.json_params}'"])

        self._call_cf


class XSUAAService(CreateService):
    def __init__(self,
                 service_name: str,
                 bound_app_name: str,
                 xs_security_template_file: str,
                 service_plan: str = 'application',
                 call_cf: Callable[[str, bool], str] = run_command
                 ) -> None:

        super().__init__(service_name, service_type='xsuaa', service_plan=service_plan, json_params=None, call_cf=call_cf)
        self._xs_security_template_file = xs_security_template_file
        self.bound_app_name = bound_app_name
        self.json_params = self.set_json_params()
        self._call_cf = call_cf

    def set_json_params(self) -> str:
        with open(self._xs_security_template_file, 'r') as f:
            place_holder_file = f.read()

        return place_holder_file.replace('APP_NAME_PLACEHOLDER', self.bound_app_name)


class PushAppWithManifest:
    def __init__(self,
                 manifest_path: str,
                 call_cf: Callable[[str, bool], str] = run_command,
                 **kwargs,
                 ) -> None:
        self.manifest_path = manifest_path
        self.kwargs = kwargs
        self._call_cf = call_cf

    def _create_app_command(self) -> str:
        c = f"cf push --manifest {self.manifest_path}"
        if self.kwargs:
            for var_name, var_value in self.kwargs.items():
                c = ' '.join([c, f"\\\n\t--var {var_name}={var_value}"])

        self._call_cf(c)

    def push_app(self) -> str:
        return self._create_app_command()


class PushAppRouter(PushAppWithManifest):
    """ Manifest needs to have defined variables `auth_service` and `auth_app_name`"""
    def __init__(self,
                 approuter_name: str,
                 baseapp_name: str,  # app to which the AppRouter will be bound
                 xsuaa_service_name: str,
                 xs_app_file_template_path: str,
                 manifest_path: str,
                 call_cf: Callable[[str, bool], str] = run_command
                 ) -> None:

        approuter_params = {
            'auth_service': xsuaa_service_name,
            'auth_app_name': approuter_name
        }
        super().__init__(manifest_path, **approuter_params)
        self.baseapp_name = baseapp_name
        self.xs_app_file_template_path = xs_app_file_template_path
        self.xs_app_file_path = xs_app_file_template_path.replace('-template.json', '.json')
        self._call_cf = call_cf

    def __create_app_descriptor(self) -> None:
        with open(self.xs_app_file_template_path, 'r') as f:
            txt_with_placeholder = f.read()

        with open(self.xs_app_file_path, 'w') as f:
            xs_app = txt_with_placeholder.replace('APP_NAME_PLACEHOLDER', self.baseapp_name)
            f.write(xs_app)

    def __remove_app_descriptor(self) -> None:
        os.remove(self.xs_app_file_path)

    def push_app(self) -> None:
        self.__create_app_descriptor()
        self._create_app_command()
        self.__remove_app_descriptor()
