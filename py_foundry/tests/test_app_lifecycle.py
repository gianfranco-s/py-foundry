from py_foundry.lib.app_lifecycle import CloudFoundryApp 


def mock_run_command(command: str) -> str:
    args = command.split()
    main_command = args[1]
    if main_command == 'apps':
        "For `cf apps` tests"
        mock_apps = ("name     requested state   processes   routes                             \n"
                     "app-1    started           web:1/1     app-1.cfapps.us10.hana.ondemand.com\n"
                     "app-2    stopped           web:0/1                                        \n"                                      
                     ""
        )
        return mock_apps
    
    elif main_command == 'set-env':
        return 'OK'

    else:
        return 'command ran'


def test_show_apps():
    app = CloudFoundryApp(call_cf=mock_run_command)
    assert app.show_apps == ('app-1', 'app-2')


def test_set_env():
    app = CloudFoundryApp(call_cf=mock_run_command)
    res = app.set_env('app-3', 'var', 'value')
    assert res == 'OK'
