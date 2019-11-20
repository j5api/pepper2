"""Pepperctl status command."""

import click
from gi.repository import GLib

from pepper2 import Pepper2


@click.command()
def status() -> None:
    """Get the status of pepper2."""

    pepper2 = Pepper2()

    try:
        print(f"Pepper2 - Robot Management Daemon v{pepper2.daemon_version}")
        print(f"\tStatus: {pepper2.daemon_status.name}")
        # statuses = controller.get_drive_statuses()
        # print(f"\t{len(statuses)} drives registered")
        # for drive in statuses:
        #     print(f"\t\t{drive}")
    except GLib.Error as e:
        if "org.freedesktop.DBus.Error.ServiceUnknown" in e.message:
            print(f"Pepper2 - Robot Management Daemon")
            print(f"\tStatus: Not Found.")
        else:
            raise
