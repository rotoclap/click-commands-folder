from pathlib import Path
import importlib.util
import sys
import types
from typing import Any
from typing import List

import click


class CommandsFolder(click.Group):
    """A ```Group``` that looks up subcommands on a folder."""

    def __init__(self, path: str, name: str | None = None, **attrs: Any) -> None:
        super().__init__(name, **attrs)

        # The folder where all module commands are stored
        self.path = Path(path)

        self.modules: dict[str, types.ModuleType] = self._load_modules()

    def _load_modules(self):
        modules = {}

        files = [
            item
            for item in self.path.iterdir()
            if (
                item.is_file()
                and item.suffix.lower() == ".py"
                and item.name.lower() != "__init__.py"
            )
        ]

        for file in files:
            module = self._import_module(f"{__package__}.{__name__}.{file.stem}", file)
            modules[file.stem] = module

        return modules

    def _import_module(self, name: str, file: Path) -> types.ModuleType:
        spec = importlib.util.spec_from_file_location(name, location=file)

        if spec is None:
            raise ValueError(f"Can't find module at {file}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module

        if spec.loader is None:
            raise ValueError(f"Can't load module from {file}")

        spec.loader.exec_module(module)

        return module

    def _load_commands(self, ctx: click.Context):
        commands = {}

        for module_name, module in self.modules.items():
            if type(module.cli) is click.Group:
                module_commands = [
                    module.cli.get_command(ctx, command_name)
                    for command_name in module.cli.list_commands(ctx)
                ]

                commands.update(
                    {
                        f"{module_name}:{command.name}": command
                        for command in module_commands
                        if command is not None
                    }
                )
            elif type(module.cli) is click.Command:
                commands.update({f"{module_name}:{module.cli.name}": module.cli})
            else:
                raise TypeError(f"Can't get commands from module {module_name}")

        for name, command in commands.items():
            self.add_command(command, name)

    def list_commands(self, ctx: click.Context) -> List[str]:
        self._load_commands(ctx)

        return sorted(self.commands)

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        self._load_commands(ctx)

        try:
            return self.commands[cmd_name]
        except KeyError:
            return None
