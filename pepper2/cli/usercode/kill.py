"""Kill usercode command."""

import click

from pepper2.api import Pepper2, Pepper2Exception


@click.command("kill")
def kill() -> None:
    """Kill running usercode."""
    try:
        pepper2 = Pepper2()
    except Pepper2Exception as e:
        click.secho(str(e), err=True, fg="red")
        exit(1)

    try:
        pepper2.kill_usercode()
        click.secho("Usercode killed successfully.", fg="green")
    except ValueError:
        click.secho(
            "Unable to kill usercode: No usercode running.",
            err=True,
            fg="red",
        )
