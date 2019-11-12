"""Pepperctl App."""

import click

from .status import status


@click.group('pepperctl')
def main() -> None:
    """Pepperctl - Control pepper2 robot management daemon."""
    pass


main.add_command(status)


if __name__ == "__main__":
    main()
