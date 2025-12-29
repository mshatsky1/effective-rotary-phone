"""CLI interface for rotary phone."""
    Enhanced with better error handling.

import click
from pathlib import Path
from typing import Optional

from rotary_phone import __version__
from rotary_phone.config import get_config_value, load_config, set_config_value
from rotary_phone.contacts import add_contact, delete_contact, get_contact, get_contact_count, list_contacts
from rotary_phone.dialer import dial
from rotary_phone.exceptions import InvalidNumberError
from rotary_phone.export import export_data, import_data
from rotary_phone.history import clear_history, get_history
from rotary_phone.stats import get_average_calls_per_day, get_dial_stats, get_top_dialed
from rotary_phone.utils import format_number, validate_number


@click.group()
@click.version_option(version=__version__)
def main():
    """Rotary Phone CLI - A simple dialing simulation tool."""
    pass


@main.command()
@click.argument("number")
@click.option("--delay", default=None, type=float, help="Delay between digits (seconds)")
@click.option("--contact", is_flag=True, help="Treat NUMBER as a contact name")
def dial_cmd(number: str, delay: Optional[float], contact: bool):
    """Dial a phone number or contact.
    
    NUMBER: Phone number to dial (supports various formats) or contact name if --contact is used
    """
    # Use default delay from config if not specified
    if delay is None:
        delay = get_config_value('default_delay', 0.1)
    
    # Try to resolve contact name if flag is set
    if contact:
        contact_number = get_contact(number)
        if not contact_number:
            click.echo(f"Error: Contact not found: {number}", err=True)
            raise click.Abort()
        formatted_contact = format_number(contact_number)
        number = contact_number
        click.echo(f"Dialing contact: {number} ({formatted_contact})")
    
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
    
    from rotary_phone.utils import format_timestamp
    click.echo(f"Recent calls (showing last {min(limit, len(history_list))}):")
    click.echo("-" * 50)
    for entry in reversed(history_list):
        timestamp = format_timestamp(entry['timestamp'])
        click.echo(f"  {entry['formatted']:<20} {timestamp}")


@main.command()
@click.option("--search", help="Search contacts by name")
def contacts(search: Optional[str]):
    """List all contacts.
    
    Use --search to filter contacts by name.
    """
    contacts_dict = list_contacts()
    
    # Filter by search term if provided
    if search:
        search_lower = search.lower()
        contacts_dict = {
            name: number for name, number in contacts_dict.items()
            if search_lower in name.lower()
        }
    
    if not contacts_dict:
        if search:
            click.echo(f"No contacts found matching '{search}'.")
        else:
            click.echo("No contacts saved.")
        return
    
    search_text = f" matching '{search}'" if search else ""
    click.echo(f"Contacts{search_text} ({len(contacts_dict)}):")
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
    
    if add_contact(name, number):
        click.echo(f"Added contact: {name} -> {number}")
    else:
        click.echo(f"Contact '{name}' already exists. Use delete command to remove it first.", err=True)
        raise click.Abort()


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
@click.argument("name")
@click.argument("number")
def update(name: str, number: str):
    """Update an existing contact's phone number.
    
    NAME: Contact name to update
    NUMBER: New phone number
    """
    from rotary_phone.contacts import update_contact
    if not validate_number(number):
        click.echo(f"Error: Invalid phone number: {number}", err=True)
        raise click.Abort()
    
    if update_contact(name, number):
        click.echo(f"Updated contact: {name} -> {number}")
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
    click.echo(f"Saved contacts: {get_contact_count()}")
    
    if stats_data['most_dialed']:
        formatted = format_number(stats_data['most_dialed'])
        click.echo(f"\nMost dialed: {formatted} ({stats_data['most_dialed_count']} times)")
        
        if top > 0:
            click.echo(f"\nTop {top} most dialed numbers:")
            top_dialed = get_top_dialed(top)
            for i, (number, count) in enumerate(top_dialed, 1):
                formatted_num = format_number(number)
                click.echo(f"  {i}. {formatted_num} - {count} time{'s' if count > 1 else ''}")
    
    # Show average calls per day
    avg_calls = get_average_calls_per_day()
    if avg_calls > 0:
        click.echo(f"\nAverage calls per day: {avg_calls:.2f}")


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


@main.group()
def config():
    """Manage configuration settings."""
    pass


@config.command()
def show():
    """Show current configuration."""
    config_data = load_config()
    click.echo("Configuration:")
    click.echo("-" * 50)
    for key, value in sorted(config_data.items()):
        click.echo(f"  {key}: {value}")


@config.command()
@click.argument("key")
@click.argument("value")
def set_cmd(key: str, value: str):
    """Set a configuration value.
    
    KEY: Configuration key
    VALUE: Configuration value
    """
    # Try to convert value to appropriate type
    try:
        if value.lower() in ('true', 'false'):
            value = value.lower() == 'true'
        elif '.' in value:
            value = float(value)
        else:
            value = int(value)
    except ValueError:
        pass  # Keep as string
    
    set_config_value(key, value)
    click.echo(f"Set {key} = {value}")

