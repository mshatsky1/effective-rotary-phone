"""CLI interface for rotary phone."""

import click

from rotary_phone import __version__


@click.group()
@click.version_option(version=__version__)
def main():
    """Rotary Phone CLI - A simple dialing simulation tool."""
    pass

