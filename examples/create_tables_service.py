import json
from time import sleep

from cf_utils import CloudFoundrySessionManager, CreateService, CreateUserProvidedService, ServiceKey
from env_management import get_cf_credentials, get_target_from_env
from log_config import logger


def create_credentials_file(env_name: str, credentials_for_file: dict) -> str:
    output_path = f'credentials/env_credentials_{env_name}.json'

    with open(output_path, 'w') as f:
        json.dump(credentials_for_file, f, indent=4)

    return output_path


def main(env_name: str) -> None:
    org, space = get_target_from_env(env_name)
    session = CloudFoundrySessionManager(org, space, *get_cf_credentials())

    service_type = 'hana'  # Full name: SAP HANA Schemas & HDI Containers
    service_plan = 'hdi-shared'
    tables_service_name = 'qas-di-hana-hdi'
    schema_name = 'QAS_DI_HDI_DB_1'

    sk = ServiceKey(org, space, *get_cf_credentials(), tables_service_name,)

    if tables_service_name in set(session.services):
        params = dict(schema=schema_name)
        tables_service = CreateService(tables_service_name, service_type, service_plan, json.dumps(params))
        logger.info(tables_service.create_service_command())

        one_minute = 60  # Not ideal. We should wait until the service is created successfully
        sleep(one_minute)

        logger.info(sk.create_service_key())

    credentials = sk.fetch_service_key_credentials()

    credentials_for_file = {
        'url': credentials.get('url'),
        'username': credentials.get('user'),
        'password': credentials.get('password')
    }

    path_to_credentials = create_credentials_file(env_name, credentials_for_file)
    params = json.dumps(credentials_for_file)
    user_provided_service = CreateUserProvidedService(f'di-{env_name}-credentials', params)
    logger.debug(user_provided_service.create_service_command())

    logger.info(f'Credentials file created: {path_to_credentials}')


if __name__ == '__main__':
    main('qas')
