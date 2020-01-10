"""Pepperctl status command."""

import click

from pepper2.api import Pepper2, Pepper2Exception


@click.command("status")
def daemon_status() -> None:
    """Get the status of pepper2."""
    try:
        pepper2 = Pepper2()
    except Pepper2Exception as e:
        click.secho(str(e), err=True, fg="red")
        exit(1)

    print(f"Pepper2 - Robot Management Daemon v{pepper2.daemon_version}")
    print(f"\tDaemon Status: {pepper2.daemon_status.name}")
    drives = pepper2.drives
    print(f"\t{len(drives)} drives currently registered.")
    for drive in drives.values():
        print(f"\t\t{drive.drive_type.name}: {drive.mount_path}")
