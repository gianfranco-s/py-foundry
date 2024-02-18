import json
import subprocess

from typing import Tuple

def run_command(command: str) -> str:
    if len(command) <= 0:
        raise ValueError('Command cannot be empty')
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    return result.stdout.rstrip('\n')


def get_cf_credentials(credentials_filepath: str) -> Tuple[str, str]:
    with open(credentials_filepath, 'r') as f:
        creds = json.load(f)
    return creds['username'], creds['password']
