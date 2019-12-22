"""Pepperd App."""
import logging

import click
from gi.repository import GLib
from pydbus import SystemBus
from systemd.daemon import notify

from pepper2 import __version__
from pepper2.status import DaemonStatus

from .controller import Controller
from .udisks_manager import UDisksManager

LOGGER = logging.getLogger(__name__)

loop = GLib.MainLoop()
# We must use the system bus, as that is where udisks is
bus = SystemBus()


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

    pepperd = PepperDaemon()

    try:
        loop.run()
    except KeyboardInterrupt:
        pepperd.stop()


class PepperDaemon:
    """The pepper2 daemon."""

    def __init__(self) -> None:
        LOGGER.info(f"Starting v{__version__}.")

        self.controller = Controller(loop)
        self.udisks_controller = UDisksManager(bus, self.controller)

        self._start()
        self.disk_signal_handler = bus.get(".UDisks2").InterfacesAdded.connect(
            self.udisks_controller.disk_signal,
        )

        self.udisks_controller.detect_initial_drives()

        self.controller.status = DaemonStatus.READY
        notify("READY=1")
        LOGGER.info(f"Ready.")

    def _start(self) -> None:
        """Start the daemon."""
        try:
            # Publish our controller on the bus.
            bus.publish("uk.org.j5.pepper2", self.controller)
        except RuntimeError as e:
            if str(e) == "name already exists on the bus":
                LOGGER.error("pepperd is already running.")
                notify("STOPPING=1")
                exit(1)
            else:
                raise

    def stop(self) -> None:
        """Stop the daemon."""
        self.controller.status = DaemonStatus.STOPPING
        notify("STOPPING=1")
        LOGGER.info("Stopping.")
        self.disk_signal_handler.disconnect()
        loop.quit()


if __name__ == "__main__":
    main()
