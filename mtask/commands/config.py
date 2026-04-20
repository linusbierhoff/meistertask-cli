from mtask.config import save_config
import click
from mtask.utils import console


@click.group()
def config():
    """Manage MeisterTask configuration."""
    pass


@config.command()
def configure():
    """Configure your MeisterTask Personal Access Token."""
    token = click.prompt(
        "Enter your MeisterTask Personal Access Token", hide_input=True
    )
    save_config(token)
    console.print("[green]Configuration saved successfully![/green]")
