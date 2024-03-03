import json
import os
from typing import Callable, Optional

from py_foundry.lib.methods import run_command
from py_foundry.lib.services import CloudFoundryService
from py_foundry.lib.apps import CloudFoundryApp

DEFAULT_SHARED_DEV_KEY_NAME = 'SharedDevKey'


class ServiceKey(CloudFoundryService):

    def __init__(self,
                 service_name: str,
                 call_cf: Callable[[str, bool], str] = run_command
                 ) -> None:
        super().__init__(call_cf)

        self.service_name = service_name

    def fetch_service_key(self, service_key_name: str = DEFAULT_SHARED_DEV_KEY_NAME) -> dict:
        service_key_text = self.service_key(self.service_name, service_key_name)
        return json.loads(service_key_text)

    def fetch_service_key_credentials(self, service_key_name: str = DEFAULT_SHARED_DEV_KEY_NAME) -> dict:
        service_key = self.fetch_service_key(service_key_name)
        return service_key.get('credentials')

    def create(self,
               json_params: Optional[str],  # Not sure why when calling this method, json_params is mandatory
               service_key_name: str = DEFAULT_SHARED_DEV_KEY_NAME,
               wait: bool = True) -> str:

        return self.create_service_key(self.service_name, service_key_name, json_params=json_params, wait=wait)

    def delete(self,
               service_key_name: str = DEFAULT_SHARED_DEV_KEY_NAME,
               force: bool = False,
               wait: bool = True) -> str:
        return self.delete_service_key(self.service_name, service_key_name, force, wait)


class CreateUserProvidedService(CloudFoundryService):
    def __init__(self,
                 service_name: str,
                 json_params: Optional[str] = None,
                 call_cf: Callable[[str, bool], str] = run_command
                 ) -> None:
        super().__init__(call_cf=call_cf)
        self.service_name = service_name
        self.json_params = json_params

    def create(self) -> str:
        return self.create_user_provided_service(self.service_name, self.json_params)

    def set_json_params_from_file(self, filepath: str) -> None:
        with open(filepath, 'r') as f:
            params = params = f.read()
        self.json_params = params


class XSUAAService(CloudFoundryService):
    def __init__(self,
                 service_name: str,
                 bound_app_name: str,
                 xs_security_template_file: str,
                 service_plan: str = 'application',
                 call_cf: Callable[[str, bool], str] = run_command) -> None:
        super().__init__(call_cf=call_cf)
        self.service_name = service_name
        self.service_type = 'xsuaa'
        self.service_plan = service_plan
        self._xs_security_template_file = xs_security_template_file
        self.bound_app_name = bound_app_name

        self.json_params = self.set_json_params()

    def set_json_params(self) -> str:
        with open(self._xs_security_template_file, 'r') as f:
            place_holder_file = f.read()

        return place_holder_file.replace('APP_NAME_PLACEHOLDER', self.bound_app_name)

    def create(self) -> str:
        self.create_service(self.service_type, self.service_plan, self.service_name, self.json_params)


class PushAppWithManifest(CloudFoundryApp):
    def __init__(self,
                 manifest_path: str,
                 call_cf: Callable[[str, bool], str] = run_command,
                 **kwargs,
                 ) -> None:
        super().__init__(call_cf=call_cf)
        self.manifest_path = manifest_path
        self.kwargs = kwargs

    def push_app(self) -> str:
        return self.push_with_manifest(self.manifest_path, **self.kwargs)


class PushAppRouter(PushAppWithManifest):
    """ Manifest needs to have defined all the variables present in `approuter_params`. """
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
            'app_name': baseapp_name,
            'auth_app_name': approuter_name,
        }
        super().__init__(manifest_path, **approuter_params, call_cf=call_cf)
        self.baseapp_name = baseapp_name
        self.xs_app_file_template_path = xs_app_file_template_path
        self.xs_app_file_path = xs_app_file_template_path.replace('-template.json', '.json')

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
        self.push_with_manifest(self.manifest_path, **self.kwargs)
        self.__remove_app_descriptor()
