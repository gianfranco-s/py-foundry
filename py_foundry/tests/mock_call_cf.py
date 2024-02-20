def mock_run_command(command: str) -> str:
    args = command.split()
    main_command = args[1]

    return {
        'apps': apps_command,
        'env': env_command,
        'set-env': set_env_command
    }.get(main_command, lambda: 'default command ran')()



def apps_command() -> str:
    mock_apps = ("name     requested state   processes   routes                             \n"
                    "app-1    started           web:1/1     app-1.cfapps.us10.hana.ondemand.com\n"
                    "app-2    stopped           web:0/1                                        \n"                                      
                    ""
    )
    return mock_apps


def env_command() -> str:
    return """
        System-Provided:
        VCAP_SERVICES: {
        "user-provided": [
            {
            "binding_guid": "guid-nr",
            "binding_name": null,
            "credentials": {
                "usr": "username",
                "pwd": "password"
            },
            "label": "user-provided"
            }
        ]
    }"""

def set_env_command() -> str:
    return 'OK'