import json
import os
from typing import Tuple

from log_config import logger

current_file_path = os.path.abspath(__file__)
CF_DIR = os.path.dirname(current_file_path)
ROOT_DIR = os.path.abspath(os.path.join(CF_DIR, os.pardir))
APP_DIR = os.path.abspath(os.path.join(ROOT_DIR, 'backend_di'))

CREDENTIALS_FILEPATH = ROOT_DIR + '/deploy_to_cloud_foundry/cf_creds.json'
XS_APP_TEMPLATE = ROOT_DIR + '/sap_approuter/xs-app-template.json'
XS_SECURITY_TEMPLATE = ROOT_DIR + '/xs-security-template.json'
APP_MANIFEST = ROOT_DIR + '/app_manifest.yml'
AUTH_APP_MANIFEST = ROOT_DIR + '/auth_app_manifest.yml'


def get_env_from_console(valid_envs: tuple = ('dev', 'qas', 'uat', 'prd')) -> str:
    logger.info(f"Please type the desired environment to deploy to: {' | '.join(valid_envs)}")
    env = input()

    if len(env) == 0:
        env = 'dev'
        logger.info(f'Using default {env=}')

    if env not in valid_envs:
        logger.error("Invalid environment. Please re-run the script.")
        exit(1)

    return env


def get_target_from_env(env_name: str) -> tuple:
    return {
        'dev': ('dev-cf-aysa', 'default2'),  # Not sure why we can't use space `obras`
        'qas': ('qas-cf-aysa', 'default'),
        'uat': ('dev-cf-aysa', 'default2'),
        'prd': ('prd-cf-aysa', 'obras'),
    }.get(env_name)


def get_cf_credentials(credentials_filepath: str = CREDENTIALS_FILEPATH) -> Tuple[str, str]:
    with open(credentials_filepath, 'r') as f:
        creds = json.load(f)
    return creds['username'], creds['password']


def get_baseadmin_email(env_name: str) -> str:
    return {
        'dev': 'dev@base.admin',
        'qas': 'gianfranco.salomone@datco.net',
        'uat': 'luis_i_llanos@aysa.com.ar',
        'prd': 'luis_i_llanos@aysa.com.ar',
    }.get(env_name)


def show_summary(**kwargs) -> None:
    summary = "\nSummary:\n"
    for k, v in kwargs.items():
        summary = ' '.join([summary, f'  {k}: {v}\n'])
    print(summary)
    logger.info(summary)
