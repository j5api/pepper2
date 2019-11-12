"""Pepperd App."""
import logging

from systemd.daemon import notify

from pepper2 import __version__

LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Main function for pepperd."""
    logging.basicConfig(level=logging.DEBUG)

    LOGGER.info(f"Starting v{__version__}.")

    notify("READY=1")
    LOGGER.info(f"Ready.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        LOGGER.info("Stopping.")


if __name__ == "__main__":
    main()
