import click
from rich.table import Table
from mtask.utils import needs_client


@click.group()
def persons():
    """Manage MeisterTask persons."""
    pass


@persons.command()
@needs_client
def me(client, console):
    """Show information about the authenticated user."""
    user = client.get_me()
    console.print("[bold]User Profile:[/bold]")
    console.print(f"ID: [cyan]{user['id']}[/cyan]")
    console.print(f"Name: [magenta]{user['firstname']} {user['lastname']}[/magenta]")
    console.print(f"Email: [blue]{user['email']}[/blue]")


@persons.command(name="list")
@click.option("--project", help="Filter by Project")
@click.option(
    "--sort",
    type=click.Choice(["id", "firstname", "lastname"]),
    default="id",
    help="Sort persons by field.",
)
@needs_client
def list_persons(client, console, project, sort):
    """List all persons."""
    persons_list = client.get_persons(project, sort)

    table = Table(
        title="MeisterTask Persons", caption=f"[bold]{len(persons_list)}[/bold] persons"
    )
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")

    for person in persons_list:
        table.add_row(str(person["id"]), f"{person['firstname']} {person['lastname']}")

    console.print(table)


@persons.command(name="get")
@click.argument("person")
@needs_client
def get_person_by_id(client, console, person):
    """Get person details by ID."""
    person_data = client.get_person_by_id(person)
    if person_data:
        console.print("[bold]Person Details:[/bold]")
        console.print(f"ID: [cyan]{person_data['id']}[/cyan]")
        console.print(
            f"Name: [magenta]{person_data['firstname']} {person_data['lastname']}[/magenta]"
        )
        console.print(f"Email: [blue]{person_data['email']}[/blue]")
    else:
        console.print(f"[yellow]Person with ID {person} not found.[/yellow]")
