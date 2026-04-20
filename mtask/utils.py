import functools
import click
from rich.console import Console
from mtask.client import MeisterTaskClient
from mtask.config import get_token

console = Console()

def needs_client(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = get_token()
        if not token:
            console.print("[red]Error:[/red] Please run [bold]'mtask configure'[/bold] first.")
            return
        
        client = MeisterTaskClient(token)
        try:
            # We inject both client and console
            return f(client, console, *args, **kwargs)
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            raise click.Abort()
    return wrapper
