"""Pepperd App."""
import logging

from gi.repository import GLib
from pydbus import SessionBus
from systemd.daemon import notify

from pepper2 import __version__
from pepper2.daemon.controller import Controller

LOGGER = logging.getLogger(__name__)

loop = GLib.MainLoop()


def main() -> None:
    """Main function for pepperd."""
    logging.basicConfig(level=logging.DEBUG)

    LOGGER.info(f"Starting v{__version__}.")

    bus = SessionBus()

    try:
        bus.publish("uk.org.j5.pepper2.Controller", Controller(loop))
    except RuntimeError as e:
        if str(e) == "name already exists on the bus":
            LOGGER.error("pepperd is already running.")
            notify("STOPPING=1")
            exit(1)
        else:
            raise

    notify("READY=1")
    LOGGER.info(f"Ready.")

    try:
        loop.run()
    except KeyboardInterrupt:
        notify("STOPPING=1")
        LOGGER.info("Stopping.")


if __name__ == "__main__":
    main()
