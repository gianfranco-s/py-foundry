from py_foundry.lib.methods import run_command
from py_foundry.lib.log_config import cf_logger

from typing import Callable


class CloudFoundryAuthenticationError(Exception):
    pass


class CloudFoundryStart:
    def __init__(self,
                 org: str,
                 space: str,
                 api_endpoint: str,
                 verbose: bool = False,
                 call_cf: Callable[[str, bool], str] = run_command) -> None:

        self.org = org
        self.space = space

        self._verbose = verbose
        self._api_endpoint = api_endpoint
        self._call_cf = call_cf

    def start_session_with_credentials(self, user: str, password: str) -> str:
        try:
            self.set_api_endpoint()
            self.login_with_credentials(user, password)
            self.set_target()
            return 'ok'

        except CloudFoundryAuthenticationError as e:
            return 'failed'

    def start_session_with_token(self) -> str:
        cf_logger.info('Get Temporary Authentication code from https://login.cf.us10.hana.ondemand.com/passcode')
        cf_logger.info('temporary code: ')
        temp_auth_token = input()

        c = f'cf login -a {self._api_endpoint} -o {self.org} -s {self.space} --sso-passcode {temp_auth_token}'
        stdout = self._call_cf(c)

        if 'OK' in stdout:
            return

        elif 'FAILED' in stdout:
            raise CloudFoundryAuthenticationError('Authentication failed')

        if self._verbose:
            cf_logger.info(f'Logging in with temporary token')
            cf_logger.info(stdout)

    def set_target(self) -> None:
        """ Target can be set after initialization. """
        stdout = self._call_cf(f'cf target -o {self.org} -s {self.space}')

        if self._verbose:
            cf_logger.info(f'Setting target:\n{stdout}')

    def login_with_credentials(self, user: str, password: str) -> None:
        c = f'cf auth {user} {password}'
        stdout = self._call_cf(c)

        if self._verbose:
            cf_logger.info(f'Logging in with user: {user} - password: {"*"*len(password)}\n')
            cf_logger.info(stdout)

        if 'OK' in stdout:
            return

        elif 'FAILED' in stdout:
            raise CloudFoundryAuthenticationError('Authentication failed')

        elif 'PASSWORD_LOCKED' in stdout:
            raise CloudFoundryAuthenticationError('Password locked. It usually gets unlocked after 1h.')

    def set_api_endpoint(self) -> None:
        stdout = self._call_cf(f'cf api {self._api_endpoint}')
        stdout = '\n'.join([stdout, 'CF CLI logs out after setting api endpoint\n'])

        if self._verbose:
            cf_logger.info(f'Setting api endpoint:\n{stdout}')
