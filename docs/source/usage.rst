Usage
=====

.. _installation:

Installation
------------

To use Click Commands Folder, first install it using pip:

.. code-block:: console

   (.venv) $ pip install click-commands-folder

Now you can instantiate ``CommandsFolder`` by giving it the folder path and eventually
a name.

How CommandsFolder works
------------------------

The ``CommandsFolder`` instance will look up in every Python file in the folder for an 
object referenced as ``cli`` (usually a function with a ``@click.command`` or
a ``@click.group`` decorator). All commands (or subcommands if ``cli`` is a ``Group``) are
added in the ``CommandsFolder`` instance to be executed.

Examples
--------

This command will be added as **cmd1:cli** in ``CommandsFolder``:

.. code-block:: python

   # filepath: app/src/commands/cmd1.py

   import click


   @click.command()
   def cli():
      ...

This command will be added as **cmd2:custom** in ``CommandsFolder``:

.. code-block:: python

   # filepath: app/src/commands/cmd2.py

   import click


   @click.command("custom")
   def cli():
      ...

This command will add 2 subcommands (**cmd_group:a** and **cmd_group:b**) in
``CommandsFolder``:

.. code-block:: python

   # filepath: app/src/commands/cmd_group.py
   import click


   @click.group("custom_group")
   def cli():
      pass


   @cli.command("a")
   def group_a():
      ...


   @cli.command("b")
   def group_b():
      ...


Using a CommandsFolder instance:

.. code-block:: python

   # filepath: app/src/cli.py

   from click_commands_folder import CommandsFolder

   if __name__ == "__main__":
      my_commands = CommandsFolder(
         "/path/where/all/commands/are/stored",
         "my commands"
      )

      my_commands()
