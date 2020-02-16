"""Pepperd App."""
import logging
from signal import SIGHUP, SIGINT, SIGTERM, Signals, signal
from types import FrameType

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

    PepperDaemon()


class PepperDaemon:
    """The pepper2 daemon."""

    def __init__(self) -> None:
        LOGGER.info(f"Starting v{__version__}.")

        # Shutdown gracefully
        signal(SIGHUP, self._signal_stop)
        signal(SIGINT, self._signal_stop)
        signal(SIGTERM, self._signal_stop)

    def stop(self) -> None:
        """Stop the daemon."""
        pass

    def _signal_stop(self, signal: Signals, __: FrameType) -> None:
        LOGGER.debug(f"Received {Signals(signal).name}")
        self.stop()


if __name__ == "__main__":
    main()
