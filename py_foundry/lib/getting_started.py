import os
import time

from py_foundry.lib.methods import run_command
from py_foundry.lib.log_config import cf_logger

from typing import Callable, Optional

__timestamp_file = 'last_execution_time.txt'
TEMPORARY_TOKEN_LENGTH = 32
DEFAULT_TOKEN_VALIDITY_SECONDS = 4*60*60


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

    def start_session_with_token(self, token_validity_seconds: Optional[int] = None) -> str:
        if is_token_still_valid(token_validity_seconds):
            cf_logger.info('Temporary authentication code is still valid')
            return
        
        temporary_auth_token_url = self._api_endpoint.replace('https://api', 'https://login', 1) + '/passcode'
        cf_logger.info(f'Get Temporary Authentication code from {temporary_auth_token_url}')
        cf_logger.info('temporary code: ')

        while True:
            temporary_auth_token = input()
            if len(temporary_auth_token) < TEMPORARY_TOKEN_LENGTH:
                cf_logger.error('Invalid token length. Please try again.')
                continue
            break

        c = f'cf login -a {self._api_endpoint} -o {self.org} -s {self.space} --sso-passcode {temporary_auth_token}'
        stdout = self._call_cf(c)

        if 'OK' in stdout:
            create_timestamp_file()  # To check the time when the user logged in
            cf_logger.info('Logged in with temporary authentication token')
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


def is_token_still_valid(valid_seconds: int, timestamp_file: str = __timestamp_file) -> bool:
    valid_seconds = valid_seconds or DEFAULT_TOKEN_VALIDITY_SECONDS

    if not os.path.exists(timestamp_file):
        return False  # If the file doesn't exist, treat it as the first run

    with open(timestamp_file, 'r') as file:
        last_execution_time = float(file.read())

    current_time = time.time()

    return current_time - last_execution_time < valid_seconds


def create_timestamp_file(timestamp_file: str = __timestamp_file) -> None:
    current_time = time.time()

    with open(timestamp_file, 'w') as file:
        file.write(str(current_time))
