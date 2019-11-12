"""Pepperctl status command."""

import click
from gi.repository import GLib
from pydbus import SessionBus


@click.command()
def status() -> None:
    """Get the status of pepper2."""
    bus = SessionBus()

    try:
        controller = bus.get("uk.org.j5.pepper2.Controller")

        print(f"Pepper2 - Robot Control Daemon v{controller.GetVersion()}")
        print(f"\tStatus: {controller.GetStatus()}")
    except GLib.Error as e:
        if "org.freedesktop.DBus.Error.ServiceUnknown" in e.message:
            click.echo("Unable to connect to pepperd.", err=True)
            click.echo("Is pepperd running?.", err=True)
        else:
            raise
