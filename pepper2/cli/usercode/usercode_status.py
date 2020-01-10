"""Usercode status command."""

import click

from pepper2.api import Pepper2, Pepper2Exception


@click.command("status")
def usercode_status() -> None:
    """Get the status of running usercode."""
    try:
        pepper2 = Pepper2()
    except Pepper2Exception as e:
        click.secho(str(e), err=True, fg="red")
        exit(1)

    print("Pepper2 Usercode Status")
    print(f"\tDaemon Status: {pepper2.daemon_status.name}")
    try:
        driver_name = pepper2.usercode_driver_name
        drive = pepper2.usercode_drive
        print(f"\tExecution Driver: {driver_name}")
        print(f"\tDrive UUID: {drive.uuid}")
        print(f"\tMount Path: {drive.mount_path}")
    except Pepper2Exception as e:
        click.secho(str(e), err=True, fg="red")
        exit(1)
    except ValueError:
        print("\tNo usercode running.")
