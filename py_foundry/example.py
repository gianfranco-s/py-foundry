from lib.login import CloudFoundryStart
from lib.cf_utils import ServiceKey
from py_foundry.lib.app_lifecycle import CloudFoundryApp
from lib.methods import get_cf_credentials

API_ENDPOINT = 'https://api.cf.us10.hana.ondemand.com'

def main() -> None:
    # org, space = ('dev-cf-aysa', 'default2')
    # cf_credentials_path = 'cf_creds.json'
    # cf_start = CloudFoundryStart(org, space, *get_cf_credentials(cf_credentials_path), API_ENDPOINT, verbose=True)
    # cf_start.start_session()

    app = CloudFoundryApp()
    # print(app.show_apps)

    # res = app.set_env('di-aysa-dev', 'test2', 'helloworld')
    # print(res)

    # res = app.env('di-aysa-dev')
    # print(res)

    sk = ServiceKey('dev-di-hana-hdi')
    # print(sk.fetch_service_key())
    # print(sk.fetch_service_key_credentials())
    print(sk.create('dev-di-hana-hdi', 'gsalomone-test', None))
    print(sk.delete('dev-di-hana-hdi', 'gsalomone-test'))
    
if __name__ == '__main__':
    main()
