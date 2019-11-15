"""Pepperctl status command."""

import click
from gi.repository import GLib
from pydbus import SystemBus


@click.command()
def status() -> None:
    """Get the status of pepper2."""
    bus = SystemBus()

    try:
        controller = bus.get("uk.org.j5.pepper2")

        print(f"Pepper2 - Robot Control Daemon v{controller.get_version()}")
        print(f"\tStatus: {controller.get_status()}")
        statuses = controller.get_drive_statuses()
        print(f"\t{len(statuses)} drives registered")
        for drive in statuses:
            print(f"\t\t{drive}")
    except GLib.Error as e:
        if "org.freedesktop.DBus.Error.ServiceUnknown" in e.message:
            click.echo("Unable to connect to pepperd.", err=True)
            click.echo("Is pepperd running?.", err=True)
        else:
            raise
