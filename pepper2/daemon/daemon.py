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
# We must use the system bus, as that is where udisks is
bus = SystemBus()


def main() -> None:
    """Main function for pepperd."""
    logging.basicConfig(level=logging.DEBUG)

    pepperd = PepperDaemon()

    try:
        loop.run()
    except KeyboardInterrupt:
        pepperd.stop()


class PepperDaemon:

    def __init__(self):
        LOGGER.info(f"Starting v{__version__}.")
        try:
            # Publish our controller on the bus.
            bus.publish("uk.org.j5.pepper2", Controller(loop))
        except RuntimeError as e:
            if str(e) == "name already exists on the bus":
                LOGGER.error("pepperd is already running.")
                notify("STOPPING=1")
                exit(1)
            else:
                raise

        # Subscribe to udisks
        self.udisks = bus.get(".UDisks2")

        self.disk_signal_handler = self.udisks.InterfacesAdded.connect(self.disk_signal)

        notify("READY=1")
        LOGGER.info(f"Ready.")

    def stop(self):
        notify("STOPPING=1")
        LOGGER.info("Stopping.")
        self.disk_signal_handler.disconnect()
        loop.quit()

    def disk_signal(self, path, data):
        LOGGER.debug(f"Received event from {path}")
        if "/org/freedesktop/UDisks2/jobs/" in path:
            for job in data.keys():
                event_data = data[job]
                if "Operation" in event_data.keys():
                    if event_data["Operation"] == "filesystem-mount":
                        LOGGER.info(f"Mount Event detected at {path}")
                        if 'Objects' in event_data.keys() and len(event_data["Objects"]) > 0:
                            disk_bus_path = event_data["Objects"][0]
                            block_device = bus.get(".UDisks2", disk_bus_path)
                            mount_points = block_device.MountPoints
                            if len(mount_points) != 0:
                                mount_point = mount_points[0]
                                chars = map(chr, mount_point)
                                mount_point_str = "".join(chars)
                                LOGGER.info(f"Drive mounted: {mount_point_str}")
                            else:
                                LOGGER.warning(f"No mountpoints available for {disk_bus_path}")
                        else:
                            LOGGER.warning("No information on drive available. Aborting.")
                    if event_data["Operation"] == "cleanup":
                        LOGGER.info(f"Removal Event detected at {path}")





if __name__ == "__main__":
    main()
