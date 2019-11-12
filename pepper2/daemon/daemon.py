"""Pepperd App."""
import logging

from gi.repository import GLib
from pydbus import SystemBus
from pydbus.bus import Bus
from systemd.daemon import notify

from pepper2 import __version__
from pepper2.daemon.controller import Controller

LOGGER = logging.getLogger(__name__)

loop = GLib.MainLoop()


def disk_signal(path, data):
    LOGGER.debug(f"Received event from {path}")
    if "/org/freedesktop/UDisks2/jobs/" in path:
        for job in data.keys():
            event_data = data[job]
            if "Operation" in event_data.keys():
                if event_data["Operation"] == "filesystem-mount":
                    LOGGER.info(f"Mount Event detected at {path}")
                    if 'Objects' in event_data.keys() and len(event_data["Objects"]) > 0:
                        print(event_data["Objects"])
                    else:
                        LOGGER.warning("No information on drive available. Aborting.")
                if event_data["Operation"] == "cleanup":
                    LOGGER.info(f"Removal Event detected at {path}")


def main() -> None:
    """Main function for pepperd."""
    logging.basicConfig(level=logging.DEBUG)

    LOGGER.info(f"Starting v{__version__}.")

    # We must use the system bus, as that is where udisks is
    bus = SystemBus()

    pepperd = PepperDaemon(bus)
    pepperd.start()

    try:
        loop.run()
    except KeyboardInterrupt:
        pepperd.stop()


class PepperDaemon:

    def __init__(self, bus: Bus):
        self.bus = Bus

    def start(self):
        try:
            # Publish our controller on the bus.
            self.bus.publish("uk.org.j5.pepper2", Controller(loop))

        except RuntimeError as e:
            if str(e) == "name already exists on the bus":
                LOGGER.error("pepperd is already running.")
                notify("STOPPING=1")
                exit(1)
            else:
                raise

        # Subscribe to udisks
        udisks = self.bus.get(".UDisks2")

        self.disk_signal_handler = udisks.InterfacesAdded.connect(disk_signal)

        notify("READY=1")
        LOGGER.info(f"Ready.")

    def stop(self):
        notify("STOPPING=1")
        LOGGER.info("Stopping.")
        self.disk_signal_handler.disconnect()
        loop.quit()


if __name__ == "__main__":
    main()
