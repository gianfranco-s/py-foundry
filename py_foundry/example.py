import json

from lib.login import CloudFoundryStart
from lib.methods import get_cf_credentials

API_ENDPOINT = 'https://api.cf.us10.hana.ondemand.com'

def main() -> None:
    org, space = ('dev-cf-aysa', 'default2')
    cf_credentials_path = 'cf_creds.json'
    session = CloudFoundryStart(org, space, *get_cf_credentials(cf_credentials_path), API_ENDPOINT, verbose=True)
    session.start_session()



    
if __name__ == '__main__':
    main()
