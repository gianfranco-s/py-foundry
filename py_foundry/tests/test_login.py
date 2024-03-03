from py_foundry.lib.getting_started import CloudFoundryStart


def mock_run_command(command: str) -> str:
    args = command.split()
    if args[1] == 'auth':
        "For `cf auth` tests"
        user = args[2]
        return 'OK' if user.startswith('valid') else 'FAILED'

    else:
        return 'command ran'


def test_login():
    cf_start = CloudFoundryStart('my-org', 'my-space', 'valid-user', 'pass', 'https://api.endpoint.com', call_cf=mock_run_command)
    res = cf_start.start_session()
    assert res == 'ok'


def test_failed_login():
    cf_start = CloudFoundryStart('my-org', 'my-space', 'user', 'pass', 'https://api.endpoint.com', call_cf=mock_run_command)
    res = cf_start.start_session()
    assert res == 'failed'
