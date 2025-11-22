"""CLI interface for rotary phone."""

import click

from rotary_phone import __version__
from rotary_phone.dialer import dial


@click.group()
@click.version_option(version=__version__)
def main():
    """Rotary Phone CLI - A simple dialing simulation tool."""
    pass


@main.command()
@click.argument("number")
@click.option("--delay", default=0.1, help="Delay between digits (seconds)")
def dial_cmd(number: str, delay: float):
    """Dial a phone number."""
    try:
        dial(number, delay)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

