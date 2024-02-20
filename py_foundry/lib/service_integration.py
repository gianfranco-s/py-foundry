from typing import Callable

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
    def show_services(self, refresh: bool = False):
        if refresh or self._services is None:
            self._services = self.__getservices()
        return self._services

    def service_key():
        # cf service-key
        """ Not implemented """

    def create_service_key():
        # cf create-service-key
        """ Not implemented """

    def create_user_provided_service():
        # cf create-user-provided-service
        """ Not implemented """

    def service_keys():
        """ Not implemented """

    def marketplace():
        """ Not implemented """

    def update_user_provided_service():
        """ Not implemented """

    def create_service():
        """ Not implemented """

    def update_service():
        """ Not implemented """

    def delete_service_key():
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
