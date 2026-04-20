import click
from rich.table import Table
from mtask.utils import needs_client


@click.group()
def sections():
    """Manage MeisterTask sections."""
    pass


@sections.command(name="list")
@click.option("--project", help="Filter by Project")
@click.option(
    "--sort",
    type=click.Choice(["id", "name"]),
    default="id",
    help="Sort sections by field.",
)
@needs_client
def list_sections(client, console, project, sort):
    """List all sections."""
    sections_data = client.get_sections(sort=sort, project=project)
    table = Table(
        title="MeisterTask Sections",
        caption=f"[bold]{len(sections_data)}[/bold] sections",
    )
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")

    for s in sections_data:
        table.add_row(str(s["id"]), s["name"])

    console.print(table)


@sections.command(name="get")
@click.argument("section")
@needs_client
def get_section_by_id(client, console, section):
    """Get section details by ID."""
    section_data = client.get_section_by_id(section)
    if section_data:
        console.print("[bold]Section Details:[/bold]")
        console.print(f"ID: [cyan]{section_data['id']}[/cyan]")
        console.print(f"Name: [magenta]{section_data['name']}[/magenta]")
    else:
        console.print(f"[yellow]Section with ID {section} not found.[/yellow]")
