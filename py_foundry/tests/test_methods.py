from pytest import raises
from py_foundry.lib.methods import run_command


def test_run_command() -> None:
    txt = 'this is a test'
    c = f'echo "{txt}"'
    assert run_command(c) == txt


def test_run_command_with_empty_command():
    with raises(ValueError) as exc_info:
        run_command('')
    assert str(exc_info.value) == 'Command cannot be empty'
