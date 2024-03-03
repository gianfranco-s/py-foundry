import json

from typing import Callable, Optional

from lib.log_config import cf_logger
from lib.methods import run_command


class CloudFoundryService:
    def __init__(self,
                 call_cf: Callable[[str, bool], str] = run_command) -> None:
        self._services = None
        self._apps = None
        self._call_cf = call_cf

    def __getservices(self) -> tuple:
        """ Return a tuple of services. """
        items_txt = self._call_cf(f'cf services | sed 1,2d')
        items_by_row = items_txt.split('\n')
        skip_titles_and_last_row = items_by_row[1:-1]  # skips titles and last, empty row
        return tuple(item.split()[0] for item in skip_titles_and_last_row)

    @property
    def show_services(self, refresh: bool = False) -> tuple:  # TODO: rename to `services`
        if refresh or self._services is None:
            self._services = self.__getservices()
        return self._services

    def service_key(self, service_instance: str, service_key: str, guid: bool = False) -> str:
        c = f'cf service-key {service_instance} {service_key}'

        if guid:
            c = ' '.join([c, '--guid'])

        c = ' | '.join([c, "sed '1,2d'"])

        return self._call_cf(c)

    def create_service_key(self,
                           service_instance: str,
                           service_key: str,
                           json_params: Optional[str],
                           wait: bool = True):
        """Create key for a service instance
        Keyword arguments:
        json_params -- json-like parameters.
        wait -- Wait for the operation to complete.
        Return: command result
        """
        c = f'cf create-service-key {service_instance} {service_key}'

        if json_params:
            c = ' '.join([c, f"-c {json.dumps(json_params)}"])

        if wait:
            c = ' '.join([c, "--wait"])

        return self._call_cf(c)

    def delete_service_key(self,
                           service_instance: str,
                           service_key: str,
                           force: bool = False,
                           wait: bool = True):
        """Delete a service key
        Keyword arguments:
        force -- requires confirmation via terminal.
        wait -- Wait for the operation to complete.
        Return: command result
        """
        c = f'cf delete-service-key {service_instance} {service_key}'

        if wait:
            c = ' '.join([c, "--wait"])

        if force:
            c = ' '.join([c, "-f"])

        else:
            cf_logger.warning(f'Please confirm deletion of service key {service_key} in service instance {service_instance} [yes/no]')
            while True:
                usr_input = input()
                if usr_input == 'yes':
                    c = ' '.join([c, "-f"])
                    break

                elif usr_input == 'no':
                    return 'aborted'

                else:
                    cf_logger.info('Valid options: [yes/no]')

        self._call_cf(c)

    def create_service(self,
                       service_type: str,
                       service_plan: str,
                       service_name: str,
                       json_params: Optional[str],
                       wait: bool = True) -> str:
        c = f"cf create-service {service_type} {service_plan} {service_name}"

        if json_params is not None:
            c = ' '.join([c, f"-c '{json_params}'"])

        if wait:
            c = ' '.join([c, "--wait"])

        return self._call_cf(c)

    def create_user_provided_service(self, service_name: str, json_params: Optional[str]) -> str:
        c = f"cf create-user-provided-service {service_name}"

        if json_params is not None:
            c = ' '.join([c, f"-p '{json_params}'"])

        return self._call_cf(c)

    def service_keys():
        """ Not implemented """

    def marketplace():
        """ Not implemented """

    def update_user_provided_service():
        """ Not implemented """

    def update_service():
        """ Not implemented """

    def delete_service():
        """ Not implemented """

    def service():
        """ Not implemented """

    def bind_service():
        """ Not implemented """

    def bind_route_service():
        """ Not implemented """

    def unbind_service():
        """ Not implemented """

    def unbind_route_service():
        """ Not implemented """
