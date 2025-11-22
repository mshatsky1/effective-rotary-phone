"""CLI interface for rotary phone."""

import click

from rotary_phone import __version__
from rotary_phone.contacts import list_contacts
from rotary_phone.dialer import dial
from rotary_phone.exceptions import InvalidNumberError
from rotary_phone.history import get_history


@click.group()
@click.version_option(version=__version__)
def main():
    """Rotary Phone CLI - A simple dialing simulation tool."""
    pass


@main.command()
@click.argument("number")
@click.option("--delay", default=0.1, help="Delay between digits (seconds)")
def dial_cmd(number: str, delay: float):
    """Dial a phone number.
    
    NUMBER: Phone number to dial (supports various formats)
    """
    try:
        dial(number, delay)
    except (ValueError, InvalidNumberError) as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.option("--limit", default=10, help="Number of recent calls to show")
def history(limit: int):
    """Show call history."""
    history_list = get_history(limit)
    if not history_list:
        click.echo("No call history.")
        return
    
    click.echo("Recent calls:")
    for entry in reversed(history_list):
        click.echo(f"  {entry['formatted']} - {entry['timestamp']}")


@main.command()
def contacts():
    """List all contacts."""
    contacts_dict = list_contacts()
    if not contacts_dict:
        click.echo("No contacts saved.")
        return
    
    click.echo("Contacts:")
    for name, number in sorted(contacts_dict.items()):
        click.echo(f"  {name}: {number}")

