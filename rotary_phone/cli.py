"""CLI interface for rotary phone."""

import click

from rotary_phone import __version__
from rotary_phone.contacts import add_contact, delete_contact, get_contact, list_contacts
from rotary_phone.dialer import dial
from rotary_phone.exceptions import InvalidNumberError
from rotary_phone.history import get_history
from rotary_phone.utils import validate_number


@click.group()
@click.version_option(version=__version__)
def main():
    """Rotary Phone CLI - A simple dialing simulation tool."""
    pass


@main.command()
@click.argument("number")
@click.option("--delay", default=0.1, help="Delay between digits (seconds)")
@click.option("--contact", is_flag=True, help="Treat NUMBER as a contact name")
def dial_cmd(number: str, delay: float, contact: bool):
    """Dial a phone number or contact.
    
    NUMBER: Phone number to dial (supports various formats) or contact name if --contact is used
    """
    # Try to resolve contact name if flag is set
    if contact:
        contact_number = get_contact(number)
        if not contact_number:
            click.echo(f"Error: Contact not found: {number}", err=True)
            raise click.Abort()
        number = contact_number
        click.echo(f"Dialing contact: {number} ({number})")
    
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


@main.command()
@click.argument("name")
@click.argument("number")
def add(name: str, number: str):
    """Add a contact.
    
    NAME: Contact name
    NUMBER: Phone number
    """
    if not validate_number(number):
        click.echo(f"Error: Invalid phone number: {number}", err=True)
        raise click.Abort()
    
    add_contact(name, number)
    click.echo(f"Added contact: {name} -> {number}")


@main.command()
@click.argument("name")
def delete(name: str):
    """Delete a contact.
    
    NAME: Contact name to delete
    """
    if delete_contact(name):
        click.echo(f"Deleted contact: {name}")
    else:
        click.echo(f"Contact not found: {name}", err=True)
        raise click.Abort()

