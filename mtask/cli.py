from mtask.commands.sections import sections
import click

from mtask.commands.config import configure
from mtask.commands.projects import projects
from mtask.commands.tasks import tasks
from mtask.commands.persons import persons


@click.group()
def cli():
    """MeisterTask CLI - Manage your projects and tasks from the terminal."""
    pass


cli.add_command(projects)
cli.add_command(sections)
cli.add_command(tasks)
cli.add_command(configure)
cli.add_command(persons)

if __name__ == "__main__":
    cli()
