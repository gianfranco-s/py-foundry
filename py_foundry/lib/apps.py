from typing import Callable, Optional

from py_foundry.lib.log_config import cf_logger
from py_foundry.lib.methods import run_command

class CloudFoundryAppLifecycleError(Exception):
    pass


class CloudFoundryApp:
    def __init__(self,
                 call_cf: Callable[[str, bool], str] = run_command) -> None:
        self._services = None
        self._apps = None
        self._call_cf = call_cf

    def __getapps(self) -> tuple:
        """ Return a tuple of apps. """
        items_txt = self._call_cf('cf apps | sed 1,2d')
        items_by_row = items_txt.split('\n')
        skip_titles_and_last_row = items_by_row[1:-1]  # skips titles and last, empty row
        return tuple(item.split()[0] for item in skip_titles_and_last_row)

    @property
    def apps(self, refresh: bool = False) -> tuple:
        if refresh or self._apps is None:
            self._apps = self.__getapps()
        return self._apps

    def set_env(self, app_name: str, variable_name: str, variable_value: str) -> str:
        c = f"cf set-env {app_name} {variable_name} '{variable_value}'"
        res = self._call_cf(c)
        return 'OK' if 'OK' in res else 'FAILED'  # TODO: return summary from _call_cf stdout

    def env(self, app_name: str) -> str:
        c = f'cf env {app_name} | sed 1d'
        return self._call_cf(c)

    def push_with_manifest(self, manifest_path: str, **kwargs) -> str:
        """Push a new app or sync changes to an existing app. Only mandatory arg is manifest_path"""
        c = f"cf push --manifest {manifest_path}"

        if kwargs:
            for var_name, var_value in kwargs.items():
                c = ' '.join([c, f"\\\n\t--var {var_name}={var_value}"])

        self._call_cf(c)

    def restart(self, app_name: str, strategy: Optional[str], no_wait: bool = False) -> str:
        """Stop all instances of the app, then start them again.

        Keyword arguments:
        app_name -- application's name
        strategy -- Deployment strategy, either rolling or null.
        no_wait -- Exit when the first instance of the web process is healthy.
        Return: result of action
        """

        c = f'cf restart {app_name}'

        # ------------ Untested ------------
        # if strategy not in ('rolling', 'null'):
        #     raise CloudFoundryAppLifecycleError('Invalid strategy')

        # if strategy:
        #     c = ' '.join([c, f'--strategy {strategy}'])

        # if no_wait:
        #     c = ' '.join([c, f'--no-wait'])

        return self._call_cf(c)

    def restage(self, app_name: str) -> str:
        """Stage the app's latest package into a droplet and restart the app with
        this new droplet and updated configuration (environment variables, service
        bindings, buildpack, stack, etc.).

        Keyword arguments: (implementation is the same as restart()
        app_name -- application's name
        strategy -- Deployment strategy, either rolling or null.
        no_wait -- Exit when the first instance of the web process is healthy.
        Return: result of action
        """

        c = f'cf restage {app_name}'

        return self._call_cf(c)

    def create_app(self, app_name: str) -> str:
        c = f'cf create-app {app_name}'

        return self._call_cf(c)

    def delete(self, app_name: str, force: bool = False, routes: bool = False) -> str:
        c = f'cf delete {app_name}'

        if routes:
            c = ' '.join([c, "-r"])

        if force:
            c = ' '.join([c, "-f"])

        else:
            cf_logger.warning(f'Please confirm deletion of app {app_name} [yes/no]')
            while True:
                usr_input = input()
                if usr_input == 'yes':
                    c = ' '.join([c, "-f"])
                    break

                elif usr_input == 'no':
                    return 'aborted'

                else:
                    cf_logger.info('Valid options: [yes/no]')

        return self._call_cf(c)

    def run_task():
        """ Not implemented """

    def logs():
        """ Not implemented """

    def ssh():
        """ Not implemented """

    def app():
        """ Not implemented """

    def scale():
        """ Not implemented """

    def events():
        """ Not implemented """

    def create_app_manifest():
        """ Not implemented """

    def apply_manifest():
        """ Not implemented """

    def revisions():
        """ Not implemented """

    def start():
        """ Not implemented """

    def stop():
        """ Not implemented """
