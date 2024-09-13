from pathlib import Path
import importlib.util
import sys
import types
from typing import Any
from typing import Dict
from typing import List

import click


class CommandsFolder(click.Group):
    """A ```Group``` that looks up subcommands on a folder."""
    def __init__(self,
                 path: str,
                 name: str | None = None,
                 **attrs: Any) -> None:
        super().__init__(name, **attrs)

        # The folder where all module commands are stored
        self.path = Path(path)

        self.commands = self._load_commands()

    def _load_command_module(self, name: str, file: Path) -> types.ModuleType:
        spec = importlib.util.spec_from_file_location(
            name,
            location=file
        )

        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)

        return module

    def _load_commands(self) -> Dict[str, click.Command]:
        """Returns all commands found in folder."""
        commands = {}

        modules_files = [
            item for item in self.path.iterdir()
            if (
                item.is_file()
                and item.suffix.lower() == ".py"
                and item.name.lower() != "__init__.py"
            )
        ]

        for file in modules_files:
            module_name = f"app.commands.{file.stem}"
            module = self._load_command_module(module_name, file)

            if isinstance(module.cli, click.Group):
                module_commands = {
                    f"{file.stem}:{module_command}": module.cli
                    for module_command in module.cli.list_commands(None)
                }

                commands.update(module_commands)
            elif isinstance(module.cli, click.Command):
                commands[f"{file.stem}:{module.cli.name}"] = module.cli
            else:
                raise TypeError(module.cli)

        return commands

    def list_commands(self, ctx: click.Context) -> List[str]:
        return sorted(self.commands)

    def get_command(self,
                    ctx: click.Context,
                    cmd_name: str) -> click.Command | None:
        if isinstance(self.commands[cmd_name], click.Group):
            return self.commands[cmd_name].get_command(
                ctx,
                cmd_name.split(":")[1])
        else:
            return self.commands[cmd_name]
