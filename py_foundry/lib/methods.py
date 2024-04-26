import json
import subprocess

from typing import Tuple


def run_command(command: str, verbose: bool = False, no_call: bool = False) -> str:
    """Run command as subprocess.

    Keyword arguments:
    command -- cf command to run
    verbose -- Default is False
    no_call -- used for debugging. Prd should be False
    Return: result of operation
    """

    if no_call:
        print(command)
        return '-- no-call --'

    if len(command) <= 0:
        raise ValueError('Command cannot be empty')
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)

    if verbose:
        print(f'stdout:\n{result.stdout}')
        print(f'stderr:\n{result.stderr}')

    return result.stdout.rstrip('\n')


def get_cf_credentials(credentials_filepath: str) -> Tuple[str, str]:
    with open(credentials_filepath, 'r') as f:
        creds = json.load(f)
    return creds['username'], creds['password']
