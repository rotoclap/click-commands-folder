import click


@click.group("group")
def cli():
    pass


@cli.command("a")
def group_a():
    print(group_a.name)


@cli.command("b")
def group_b():
    print(group_b.name)
