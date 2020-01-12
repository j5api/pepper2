"""Pepperd App."""
import logging
from signal import SIGHUP, SIGINT, SIGTERM, Signals, signal
from time import sleep
from types import FrameType

import click
from gi.repository import GLib
from pydbus import SystemBus
from systemd.daemon import notify

from pepper2 import __version__
from pepper2.common.daemon_status import DaemonStatus
from pepper2.daemon.dbus.controller import Controller

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

        self.controller = Controller(loop, bus)
        self.udisks_manager = UDisksManager(bus, self.controller)

        try:
            # Publish our controller on the bus.
            self.controller_object = bus.publish("uk.org.j5.pepper2", self.controller)
        except RuntimeError as e:
            if str(e) == "name already exists on the bus":
                LOGGER.error("pepperd is already running.")
                notify("STOPPING=1")
                exit(1)
            else:
                raise

        self.disk_signal_handler = bus.get(".UDisks2").InterfacesAdded.connect(
            self.udisks_manager.disk_signal,
        )

        # Shutdown gracefully
        signal(SIGHUP, self._signal_stop)
        signal(SIGINT, self._signal_stop)
        signal(SIGTERM, self._signal_stop)

        self.udisks_manager.detect_initial_drives()

        if self.controller.daemon_status is DaemonStatus.STARTING:
            # Only change the status if a usercode hasn't started.
            self.controller.daemon_status = DaemonStatus.READY

        notify("READY=1")
        LOGGER.info(f"Ready.")

    def stop(self) -> None:
        """Stop the daemon."""
        notify("STOPPING=1")
        LOGGER.info("Stopping.")

        # Disconnect from D-Bus
        self.disk_signal_handler.disconnect()
        self.controller_object.unpublish
        sleep(0.3)  # Wait, just in case usercode has only just started.

        if self.controller.usercode_driver is not None:
            self.controller.usercode_driver.stop_execution()

        loop.quit()
        LOGGER.info("Stopped.")

    def _signal_stop(self, signal: Signals, __: FrameType) -> None:
        LOGGER.debug(f"Received {Signals(signal).name}")
        self.stop()


if __name__ == "__main__":
    main()
