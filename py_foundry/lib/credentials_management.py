import json

from typing import Tuple


def get_cf_credentials(credentials_filepath: str) -> Tuple[str, str]:
    with open(credentials_filepath, 'r') as f:
        creds = json.load(f)
    return creds['username'], creds['password']
