import json

from lib.cf_utils import ServiceKey
from lib.log_config import cf_logger


def get_vcap(credentials: dict, tables_service_name: str, org: str, space: str, service_key_name: str) -> dict:
    return {
        'hana': [{
            'name': 'hana-hdi',
            'instance_name': tables_service_name,
            'label': tables_service_name,
            'tags':
                ['hana', 'database', 'relational', 'mta-resource-name:hdi_db',
                    'endpoint:https://api.cf.us10.hana.ondemand.com', f'org:{org}',
                    f'space:{space}'],
            'plan': 'hdi-shared',
            'credentials': {
                'service_key_name': service_key_name,
                'host': credentials.get('host'),
                'port': credentials.get('port'),
                'driver': credentials.get('driver'),
                'url': credentials.get('url'),
                'schema': credentials.get('schema'),
                'hdi_user': credentials.get('hdi_user'),
                'hdi_password': credentials.get('hdi_password'),
                'user': credentials.get('user'),
                'password': credentials.get('password'),
                'certificate': credentials.get('certificate')
                }
            }]
        }


def get_vcap_services(org: str,
                      space: str,
                      env_name: str = 'dev',
                      output_file_prefix: str = 'hana-env-credentials-{env_name}.env'
                      ) -> None:
    cf_logger.info('Fetching env file to deploy objects in SAP BAS')

    tables_service_name = f'{env_name}-di-hana-hdi'

    sk = ServiceKey(tables_service_name)

    service_key_name = 'SharedDevKey'
    credentials = sk.fetch_service_key_credentials(service_key_name)

    vcap = get_vcap(credentials, tables_service_name, org, space, service_key_name)
    vcap_json = json.dumps(vcap, indent=4)
    cf_logger.debug(f'JSON data for env variable:\n{vcap_json}')

    vcap_services = f"VCAP_SERVICES='{vcap_json}'"

    with open(output_file_prefix.format(env_name=env_name), 'w') as f:
        f.write(vcap_services)
