import json

from py_foundry.lib.getting_started import CloudFoundryStart
from py_foundry.lib.cf_utils import ServiceKey
from py_foundry.lib.apps import CloudFoundryApp
from py_foundry.lib.methods import get_cf_credentials

API_ENDPOINT = 'https://api.cf.us10.hana.ondemand.com'


def create_credentials_file(env_name: str) -> str:
    CloudFoundryStart('prd-cf-aysa', 'default', *get_cf_credentials('cf_creds.json'), API_ENDPOINT).start_session()
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


def main() -> None:
    # org, space = ('dev-cf-aysa', 'default2')
    # cf_credentials_path = 'cf_creds.json'
    # cf_start = CloudFoundryStart(org, space, *get_cf_credentials(cf_credentials_path), API_ENDPOINT, verbose=True)
    # cf_start.start_session()

    app = CloudFoundryApp()
    # print(app.show_apps)

    # res = app.set_env('di-aysa-dev', 'test2', 'helloworld')
    # print(res)

    res = app.env('di-aysa-stg')
    print(res)

    # sk = ServiceKey('dev-di-hana-hdi')
    # print(sk.fetch_service_key())
    # print(sk.fetch_service_key_credentials())
    # print(sk.create('dev-di-hana-hdi', 'gsalomone-test', None))
    # print(sk.delete('dev-di-hana-hdi', 'gsalomone-test'))


if __name__ == '__main__':
    main()
    # create_credentials_file('prd')
