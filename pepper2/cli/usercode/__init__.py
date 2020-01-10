"""Usercode commands."""

import click

from .usercode_status import usercode_status


@click.group()
def usercode() -> None:
    """Interact with and query running usercode."""
    pass


usercode.add_command(usercode_status)
