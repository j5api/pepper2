"""Pepperd App."""
import logging

import click
import uvicorn

from pepper2 import __version__
from pepper2.daemon.daemon import PepperDaemon

from .api import core_router

LOGGER = logging.getLogger(__name__)

app = PepperDaemon()

app.include_router(core_router)


@click.command("pepperd")
@click.option('--port', type=int, default=7032, help="Bind server to port.")  # "p2"=7032
@click.option('--host', type=str, default="localhost", help="Bind server to host.")
@click.option('-v', '--verbose', is_flag=True, help="Enable verbose logging.")
@click.option('--dev', is_flag=True, help="Enable development mode.")
def main(
        *,
        port: int,
        host: str,
        verbose: bool,
        dev: bool,
) -> None:
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
    uvicorn.run(
        'pepper2.daemon.app:app',
        host=host,
        port=port,
        debug=dev,
        reload=dev,
        workers=1,  # Exactly one worker.
    )


if __name__ == "__main__":
    main()
