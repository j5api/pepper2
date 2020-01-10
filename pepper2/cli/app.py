"""Pepperctl App."""

import click

from .daemon_status import daemon_status
from .usercode import usercode


@click.group('pepperctl')
def main() -> None:
    """Pepperctl - Control pepper2 robot management daemon."""
    pass


main.add_command(daemon_status)
main.add_command(usercode)

if __name__ == "__main__":
    main()
