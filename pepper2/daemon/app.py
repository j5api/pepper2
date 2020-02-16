"""Pepperd App."""
import logging

import click

from pepper2 import __version__

LOGGER = logging.getLogger(__name__)


@click.command("pepperd")
@click.option('-v', '--verbose', is_flag=True)
def main(*, verbose: bool) -> None:
    """Pepper2 Daemon."""
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    LOGGER.info(f"Starting v{__version__}.")


if __name__ == "__main__":
    main()
