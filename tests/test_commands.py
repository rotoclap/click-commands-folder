from pathlib import Path

import click

from click_commands_folder.commands_folder import CommandsFolder

testdir = Path(__file__).parent


def test_list_commands():
    cli = CommandsFolder(testdir / "fixtures/commands", "test")

    commands = cli.list_commands(None)

    assert set(commands) == {
        "command_b:custom_name",
        "command_a:cli",
        "command_group:a",
        "command_group:b"
    }


def test_get_command():
    cli = CommandsFolder(testdir / "fixtures/commands", "test")

    command = cli.get_command(None, "command_b:custom_name")

    assert isinstance(command, click.Command)
    assert command.name == "custom_name"
