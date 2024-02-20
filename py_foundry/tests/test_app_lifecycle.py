from py_foundry.lib.app_lifecycle import CloudFoundryApp 
from py_foundry.tests.mock_call_cf import mock_run_command

def test_show_apps():
    app = CloudFoundryApp(call_cf=mock_run_command)
    assert app.show_apps == ('app-1', 'app-2')


def test_set_env():
    app = CloudFoundryApp(call_cf=mock_run_command)
    res = app.set_env('app-3', 'var', 'value')
    assert res == 'OK'

def test_get_env():
    app = CloudFoundryApp(call_cf=mock_run_command)
    res = app.env('app-3')
    assert 'System-Provided:' in res
