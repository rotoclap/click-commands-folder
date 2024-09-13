import click


@click.command("custom_name")
def cli():
    return cli.name
