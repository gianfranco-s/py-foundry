from pytest import raises
from py_foundry.lib.methods import run_command


def test_run_command() -> None:
    txt = 'this is a test'
    c = f'echo "{txt}"'
    assert run_command(c, no_call=False) == txt


def test_run_command_with_empty_command():
    with raises(ValueError) as exc_info:
        run_command('', no_call=False)
    assert str(exc_info.value) == 'Command cannot be empty'
