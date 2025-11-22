"""CLI interface for rotary phone."""

import click

import click
from pathlib import Path

from rotary_phone import __version__
from rotary_phone.contacts import add_contact, delete_contact, get_contact, list_contacts
from rotary_phone.dialer import dial
from rotary_phone.exceptions import InvalidNumberError
from rotary_phone.export import export_data, import_data
from rotary_phone.history import clear_history, get_history
from rotary_phone.stats import get_dial_stats, get_top_dialed
from rotary_phone.utils import format_number, validate_number


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
    
    click.echo(f"Recent calls (showing last {min(limit, len(history_list))}):")
    click.echo("-" * 50)
    for entry in reversed(history_list):
        timestamp = entry['timestamp'][:19].replace('T', ' ')
        click.echo(f"  {entry['formatted']:<20} {timestamp}")


@main.command()
def contacts():
    """List all contacts."""
    contacts_dict = list_contacts()
    if not contacts_dict:
        click.echo("No contacts saved.")
        return
    
    click.echo(f"Contacts ({len(contacts_dict)}):")
    click.echo("-" * 50)
    for name, number in sorted(contacts_dict.items()):
        formatted = format_number(number)
        click.echo(f"  {name:<20} {formatted}")


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


@main.command()
@click.confirmation_option(prompt="Are you sure you want to clear call history?")
def clear():
    """Clear call history."""
    clear_history()
    click.echo("Call history cleared.")


@main.command()
@click.option("--top", default=5, help="Number of top dialed numbers to show")
def stats(top: int):
    """Show dialing statistics."""
    stats_data = get_dial_stats()
    
    click.echo("Statistics:")
    click.echo("-" * 50)
    click.echo(f"Total calls: {stats_data['total_calls']}")
    click.echo(f"Unique numbers: {stats_data['unique_numbers']}")
    click.echo(f"Saved contacts: {stats_data['total_contacts']}")
    
    if stats_data['most_dialed']:
        formatted = format_number(stats_data['most_dialed'])
        click.echo(f"\nMost dialed: {formatted} ({stats_data['most_dialed_count']} times)")
        
        if top > 0:
            click.echo(f"\nTop {top} most dialed numbers:")
            top_dialed = get_top_dialed(top)
            for i, (number, count) in enumerate(top_dialed, 1):
                formatted_num = format_number(number)
                click.echo(f"  {i}. {formatted_num} - {count} time{'s' if count > 1 else ''}")


@main.command()
@click.argument("output_file", type=click.Path())
@click.option("--no-history", is_flag=True, help="Exclude history from export")
def export(output_file: str, no_history: bool):
    """Export contacts and history to a JSON file.
    
    OUTPUT_FILE: Path to the output JSON file
    """
    output_path = Path(output_file)
    export_data(output_path, include_history=not no_history)
    click.echo(f"Data exported to {output_file}")


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--replace", is_flag=True, help="Replace existing data instead of merging")
def import_cmd(input_file: str, replace: bool):
    """Import contacts and history from a JSON file.
    
    INPUT_FILE: Path to the input JSON file
    """
    input_path = Path(input_file)
    stats = import_data(input_path, merge=not replace)
    
    click.echo("Import complete:")
    click.echo(f"  Contacts added: {stats['contacts_added']}")
    if stats['contacts_skipped'] > 0:
        click.echo(f"  Contacts skipped: {stats['contacts_skipped']}")
    click.echo(f"  History entries added: {stats['history_entries_added']}")

