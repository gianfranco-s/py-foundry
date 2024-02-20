from typing import Callable, Optional

from lib.methods import run_command


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
        items_txt = self._call_cf(f'cf apps | sed 1,2d')
        items_by_row = items_txt.split('\n')
        skip_titles_and_last_row = items_by_row[1:-1]  # skips titles and last, empty row
        return tuple(item.split()[0] for item in skip_titles_and_last_row)

    @property
    def show_apps(self, refresh: bool = False):
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

    def push():
        """ Tentatively implemented with the class PushAppWithManifest
        Maybe build that class as a child of CloudFoundryApp
        """

    def restart(self, app_name: str, strategy: Optional[str], no_wait: Optional[bool]) -> str:
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

    def run_task():
        """ Not implemented """

    def logs():
        """ Not implemented """

    def ssh():
        """ Not implemented """

    def app():
        """ Not implemented """

    def delete():
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
