from py_foundry.lib.login import CloudFoundryStart, CloudFoundryAuthenticationError


def mock_run_command(command: str) -> str:
    args = command.split()
    if args[1] == 'auth':
        "For `cf auth` tests"
        user = args[2]
        return 'ok' if user.startswith('valid') else 'failed'

    else:
        return 'command ran'


def test_login():
    session = CloudFoundryStart('my-org', 'my-space', 'user', 'pass', 'https://api.endpoint.com', verbose=True, call_cf=mock_run_command)
    res = session.start_session()
    assert res == 'ok'


def test_failed_login():
    session = CloudFoundryStart('my-org', 'my-space', 'user', 'invalid-pass', 'https://api.endpoint.com')
    res = session.start_session()
    assert res == 'failed'
