from pathlib import Path

import click

from click_commands_folder.commands_folder import CommandsFolder

testdir = Path(__file__).parent


def test_load_modules():
    cli = CommandsFolder(testdir / "fixtures/commands", "test")

    assert set(cli.modules.keys()) == {"command_b", "command_a", "command_group"}


def test_load_commands():
    cli = CommandsFolder(testdir / "fixtures/commands", "test")
    cli._load_commands(None)

    assert set(cli.commands) == {
        "command_b:custom_name",
        "command_a:cli",
        "command_group:a",
        "command_group:b",
    }

    for command in cli.commands.values():
        assert type(command) is click.Command


def test_list_commands():
    cli = CommandsFolder(testdir / "fixtures/commands", "test")

    assert set(cli.list_commands(None)) == {
        "command_b:custom_name",
        "command_a:cli",
        "command_group:a",
        "command_group:b",
    }


def test_get_command():
    cli = CommandsFolder(testdir / "fixtures/commands", "test")

    command = cli.get_command(None, "command_b:custom_name")

    assert type(command) is click.Command
    assert command.name == "custom_name"
