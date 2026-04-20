import click
from rich.table import Table
from mtask.utils import needs_client


@click.group()
def tasks():
    """Manage MeisterTask tasks."""
    pass


@tasks.command(name="list")
@click.option("--mine", is_flag=True, help="List only tasks assigned to me.")
@click.option("--unassigned", is_flag=True, help="List only unassigned tasks.")
@click.option("--project", help="Filter by Project")
@click.option("--section", help="Filter by Section")
@click.option(
    "--sort",
    type=click.Choice(["id", "name", "section", "assigned"]),
    default="id",
    help="Sort tasks by field.",
)
@needs_client
def list_tasks(client, console, mine, unassigned, project, section, sort):
    """List tasks."""

    if sort == "section":
        sort = "section_id"
    elif sort == "assigned":
        sort = "assigned_to_id"

    tasks_data = client.get_tasks(
        assigned_to_me=mine,
        unassigned=unassigned,
        project=project,
        section=section,
        sort=sort,
    )

    table = Table(
        title="MeisterTask Tasks", caption=f"[bold]{len(tasks_data)}[/bold] tasks"
    )
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Section", style="green")
    table.add_column("Assigned", style="blue")

    for t in tasks_data:
        table.add_row(
            str(t["id"]),
            t["name"],
            t.get("section_name", "Unknown"),
            t.get("assigned_to_name", "Unassigned"),
        )

    console.print(table)


@tasks.command(name="get")
@click.argument("task")
@needs_client
def get_task_by_id(client, console, task):
    """Get task details by ID."""
    task_data = client.get_task_by_id(task)
    if task_data:
        console.print("[bold]Task Details:[/bold]")
        console.print(f"ID: [cyan]{task_data['id']}[/cyan]")
        console.print(f"Name: [magenta]{task_data['name']}[/magenta]")
        console.print(
            f"Section: [green]{task_data.get('section_name', 'Unknown')}[/green]"
        )
        console.print(
            f"Assigned: [blue]{task_data.get('assigned_to_name', 'Unassigned')}[/blue]"
        )
    else:
        console.print(f"[yellow]Task with ID {task} not found.[/yellow]")


@tasks.command()
@click.option("--name", required=True, help="Name of the task.")
@click.option("--section", required=True, help="Section to create the task in.")
@click.option("--project", help="Project to create the task in.")
@needs_client
def create(client, console, section, name, project):
    """Create a new task."""
    task = client.create_task(name=name, section=section, project=project)
    console.print(f"[green]Task created![/green] ID: [cyan]{task['id']}[/cyan]")


@tasks.command()
@click.argument("task")
@click.option("--section", required=True, help="New section for the task.")
@needs_client
def edit(client, console, task, section):
    """Edit a task."""
    client.move_task(task, section)
    console.print(
        f"[green]Task [cyan]{task}[/cyan] moved to section [cyan]{section}[/cyan]![/green]"
    )
