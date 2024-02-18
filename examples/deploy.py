import json

from cf_utils import CloudFoundrySessionManager, PushAppRouter, PushAppWithManifest, XSUAAService
from env_management import (APP_MANIFEST,
                            AUTH_APP_MANIFEST,
                            XS_APP_TEMPLATE,
                            XS_SECURITY_TEMPLATE,
                            get_baseadmin_email,
                            get_cf_credentials,
                            get_target_from_env,
                            show_summary,)
from log_config import logger


def main(env_name: str, base_app_name: str = 'di-aysa-') -> None:

    session = CloudFoundrySessionManager(*get_target_from_env(env_name),
                                         *get_cf_credentials())

    logger.debug(f'org: {session.org}, space: {session.space}')

    app_name = f"{base_app_name}{env_name}"
    auth_app_name = f'di-aysa-{env_name}'
    xsuaa_service_name = f'di-aysa-pyuaa-{env_name}'
    tables_service_name = f'di-{env_name}-credentials'
    baseadmin_email = get_baseadmin_email(env_name)

    if xsuaa_service_name not in set(session.services):
        xsuaa_service = XSUAAService(xsuaa_service_name, app_name, XS_SECURITY_TEMPLATE)
        c = xsuaa_service.create_service_command()
        logger.debug(c)

    app_vars = {
        'app_name': app_name,
        'tables_service': tables_service_name,
        'flask_debug': env_name == 'dev',
        'auth_service': xsuaa_service_name,
        'baseadmin_email': baseadmin_email
    }
    app = PushAppWithManifest(manifest_path=APP_MANIFEST, **app_vars)
    c = app.push_app()
    logger.debug(c)

    if auth_app_name not in set(session.apps):
        logger.info(session.create_app(auth_app_name))
        destinations_json = [{
            'name': app_name,
            'url': f'https://{app_name}.cfapps.us10.hana.ondemand.com/',
            'forwardAuthToken': True
        }]
        logger.info(session.set_env(auth_app_name, 'destinations', json.dumps(destinations_json)))
        auth_app = PushAppRouter(auth_app_name,
                                 app_name,
                                 xsuaa_service_name,
                                 XS_APP_TEMPLATE,
                                 AUTH_APP_MANIFEST)
        c = auth_app.push_app()
        logger.debug(c)

    show_summary(app_name=app_name,
                 auth_app_name=auth_app_name,
                 xsuaa_service_name=xsuaa_service_name,
                 tables_service_name=tables_service_name,
                 baseadmin_email=baseadmin_email,
                 )


if __name__ == '__main__':
    main('dev')
