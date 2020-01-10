"""Usercode commands."""

import click

from .kill import kill
from .usercode_status import usercode_status


@click.group()
def usercode() -> None:
    """Interact with and query running usercode."""
    pass


usercode.add_command(kill)
usercode.add_command(usercode_status)
