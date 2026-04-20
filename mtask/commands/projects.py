import click
from rich.table import Table
from mtask.utils import needs_client


@click.group()
def projects():
    """Manage MeisterTask projects."""
    pass


@projects.command(name="list")
@click.option(
    "--sort",
    type=click.Choice(["id", "name"]),
    default="id",
    help="Sort projects by field.",
)
@needs_client
def list_projects(client, console, sort):
    """List all projects."""
    projects_data = client.get_projects(sort)
    table = Table(
        title="MeisterTask Projects", caption=f"[bold]{len(projects_data)}[/bold] projects"
    )
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")

    for p in projects_data:
        table.add_row(str(p["id"]), p["name"])

    console.print(table)


@projects.command(name="get")
@click.argument("project")
@needs_client
def get_project_by_id(client, console, project):
    """Get project details by ID."""
    project_data = client.get_project_by_id(project)
    if project_data:
        console.print("[bold]Project Details:[/bold]")
        console.print(f"ID: [cyan]{project_data['id']}[/cyan]")
        console.print(f"Name: [magenta]{project_data['name']}[/magenta]")
    else:
        console.print(f"[yellow]Project with ID {project} not found.[/yellow]")
