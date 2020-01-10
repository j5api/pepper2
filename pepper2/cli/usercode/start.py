"""Start usercode command."""

import click

from pepper2.api import Pepper2, Pepper2Exception


@click.command("start")
def start() -> None:
    """Start dead usercode."""
    try:
        pepper2 = Pepper2()
    except Pepper2Exception as e:
        click.secho(str(e), err=True, fg="red")
        exit(1)

    try:
        pepper2.start_usercode()
        click.secho("Usercode started successfully.", fg="green")
    except ValueError as e:
        click.secho(
            f"Unable to start usercode: {e}",
            err=True,
            fg="red",
        )
