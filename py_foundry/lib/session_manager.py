from typing import Callable

from methods import run_command


class CloudFoundrySession:
    def __init__(self,
                 call_cf: Callable[[str, bool], str] = run_command) -> None:
        self._services = None
        self._apps = None
        self._call_cf = call_cf

    def __getitems(self, items_name: 'str') -> tuple:
        """ Return a tuple of services. We're only using part of the cf `items` command
        Only `items` allowed: `services`, `apps`
        """
        items_txt = self._call_cf(f'cf {items_name} | sed 1,2d')
        items_by_row = items_txt.split('\n')[1:-1]  # skip titles and last, empty row
        return tuple(item.split()[0] for item in items_by_row)

    @property
    def services(self, refresh: bool = False):
        if refresh or self._services is None:
            self._services = self.__getitems('services')
        return self._services

    @property
    def apps(self, refresh: bool = False):
        if refresh or self._apps is None:
            self._apps = self.__getitems('apps')
        return self._apps

    def set_env(self, app_name: str, variable_name: str, variable_value: str) -> str:
        c = f"cf set-env {app_name} {variable_name} '{variable_value}'"
        self._call_cf(c)
