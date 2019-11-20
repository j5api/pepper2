"""
Udisks2 Controller.

Abstract and talk to UDisks.
"""
import logging
from pathlib import Path
from time import sleep
from typing import Dict

from pydbus.bus import Bus

from pepper2.drives import Drive, DriveType

from .controller import Controller

LOGGER = logging.getLogger(__name__)


class UDisksController:
    """Talk to UDisks2 over D-Bus."""

    def __init__(self, bus: Bus, controller: Controller):
        self.bus = bus
        self.controller = controller

    def disk_signal(self, path: str, data: Dict[str, Dict[str, str]]) -> None:
        """Handle a disk signal event from UDisks2."""
        LOGGER.debug(f"Received event from {path}")
        if "/org/freedesktop/UDisks2/jobs/" in path:
            for job in data.keys():
                event_data = data[job]
                if "Operation" in event_data.keys():
                    if event_data["Operation"] == "filesystem-mount":
                        LOGGER.info(f"Mount Event detected at {path}")
                        sleep(0.3)
                        self.handle_mount_event(event_data)

                    if event_data["Operation"] == "cleanup":
                        LOGGER.info(f"Removal Event detected at {path}")
                        sleep(0.3)
                        self.handle_cleanup_event(event_data)

    def handle_mount_event(self, event_data: Dict[str, str]) -> None:
        """Handle a mount event."""
        if 'Objects' in event_data.keys() \
                and len(event_data["Objects"]) > 0:
            disk_bus_path = event_data["Objects"][0]
            block_device = self.bus.get(".UDisks2", disk_bus_path)
            mount_points = block_device.MountPoints
            if len(mount_points) != 0:
                # We are only interested in the first mountpoint.
                mount_point = mount_points[0]

                # Data is null terminated.
                mount_point = mount_point[:len(mount_point) - 1]

                chars = map(chr, mount_point)
                mount_point_str = "".join(chars)
                mount_path = Path(mount_point_str)

                if mount_path.exists():
                    drive = Drive(
                        uuid=block_device.UUID,
                        mount_path=mount_path,
                        drive_type=DriveType.NO_ACTION,  # Ignore everything for now.
                    )
                    LOGGER.info(f"Drive {drive.uuid} mounted: {drive.mount_path}")
                    with self.controller.data_lock:
                        self.controller.drive_group[drive.uuid] = drive
                else:
                    LOGGER.warning(
                        f"Unreadable drive mounted: {mount_path}",
                    )
            else:
                LOGGER.warning(
                    f"No mountpoints available for {disk_bus_path}",
                )
        else:
            LOGGER.warning("No information on drive available. Aborting.")

    def handle_cleanup_event(self, _: Dict[str, str]) -> None:
        """Handle a cleanup event."""
        with self.controller.data_lock:
            # We have no information to tell which drive left.
            # Thus we need to check.
            removed_drives = []
            for drive in self.controller.drive_group.values():
                if not drive.mount_path.exists():
                    LOGGER.info(f"Drive removed: {drive.uuid }({drive.mount_path})")
                    removed_drives.append(drive.uuid)
            for uuid in removed_drives:
                self.controller.drive_group.pop(uuid)
