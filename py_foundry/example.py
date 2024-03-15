import json

from py_foundry.lib.getting_started import CloudFoundryStart
from py_foundry.lib.cf_utils import ServiceKey
from py_foundry.lib.apps import CloudFoundryApp
from py_foundry.lib.services import CloudFoundryService
from py_foundry.lib.methods import get_cf_credentials

API_ENDPOINT = 'https://api.cf.us10.hana.ondemand.com'


def create_credentials_file(env_name: str) -> str:
    CloudFoundryStart('prd-cf-aysa', 'default', *get_cf_credentials('cf_creds.json'), API_ENDPOINT).start_session_with_credentials()
    sk = ServiceKey('prd-di-hana-hdi')
    credentials = sk.fetch_service_key_credentials()

    credentials_for_file = {
        'url': credentials.get('url'),
        'username': credentials.get('user'),
        'password': credentials.get('password')
    }

    output_path = f'env_credentials_{env_name}.json'

    with open(output_path, 'w') as f:
        json.dump(credentials_for_file, f, indent=4)

    return output_path


def session_init_with_credentials() -> None:
    cf_credentials_path = 'cf_creds.json'
    cf_start = CloudFoundryStart(org='dev-cf-aysa', space='default2', api_endpoint=API_ENDPOINT, verbose=True)
    cf_start.start_session_with_credentials(*get_cf_credentials(cf_credentials_path))


def session_init_with_token() -> None:
    cf_start = CloudFoundryStart(org='dev-cf-aysa', space='default2', api_endpoint=API_ENDPOINT, verbose=True)
    cf_start.start_session_with_token()


def envs() -> None:
    app = CloudFoundryApp()

    res = app.set_env(app_name='di-aysa-dev', variable_name='test2', variable_value='helloworld')
    print(res)

    res = app.env(app_name='di-aysa-dev')
    print(res)


def service_keys() -> None:
    sk = ServiceKey(service_name='dev-di-hana-hdi')
    print(sk.fetch_service_key())
    print(sk.fetch_service_key_credentials())


def delete_app():
    app = CloudFoundryApp()
    app.delete(app_name='py-presid-dev', force=True)


def delete_service():
    service = CloudFoundryService()
    res = service.delete_service(service_name='py-presid-ups-dev', force=True)
    print(res)


if __name__ == '__main__':
    session_init_with_token()
    # envs()
    # service_keys()
    # create_credentials_file('prd')
    # delete_app()
    delete_service()
