"""Pepperctl status command."""

import click

from pepper2 import Pepper2


@click.command()
def status() -> None:
    """Get the status of pepper2."""
    pepper2 = Pepper2()

    print(f"Pepper2 - Robot Management Daemon v{pepper2.daemon_version}")
    print(f"\tStatus: {pepper2.daemon_status.name}")
    # statuses = controller.get_drive_statuses()
    # print(f"\t{len(statuses)} drives registered")
    # for drive in statuses:
    #     print(f"\t\t{drive}")
