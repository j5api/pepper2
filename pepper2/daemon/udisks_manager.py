"""
Udisks2 Controller.

Abstract and talk to UDisks.
"""
import logging
from pathlib import Path
from time import sleep
from typing import Dict, List

from pydbus.bus import Bus

from pepper2.drives import Drive, DriveType

from .controller import Controller

LOGGER = logging.getLogger(__name__)


class UDisksManager:
    """Talk to UDisks2 over D-Bus."""

    def __init__(self, bus: Bus, controller: Controller):
        self.bus = bus
        self.controller = controller

    @staticmethod
    def bytes_to_path(data: List[int]) -> Path:
        """Convert a null terminated int array to a path."""
        # Data is null terminated.
        mount_point = data[:len(data) - 1]

        chars = [chr(x) for x in mount_point]
        mount_point_str = "".join(chars)

        return Path(mount_point_str)

    def disk_signal(self, path: str, data: Dict[str, Dict[str, str]]) -> None:
        """Handle a disk signal event from UDisks2."""
        LOGGER.debug(f"Received event from {path}")

        if path.startswith("/org/freedesktop/UDisks2/jobs/"):
            for job in data.keys():
                event_data = data[job]
                if "Operation" in event_data.keys():
                    if event_data["Operation"] == "filesystem-mount":
                        LOGGER.debug(f"Mount Event detected at {path}")
                        sleep(0.3)
                        self._handle_mount_event(event_data)

                    if event_data["Operation"] == "cleanup":
                        LOGGER.debug(f"Removal Event detected at {path}")
                        sleep(0.3)
                        self._handle_cleanup_event(event_data)

    def _handle_mount_event(self, event_data: Dict[str, str]) -> None:
        """Handle a mount event."""
        if 'Objects' in event_data.keys() \
                and len(event_data["Objects"]) > 0:
            disk_bus_path = event_data["Objects"][0]
            block_device = self.bus.get(".UDisks2", disk_bus_path)
            mount_points = block_device.MountPoints
            if len(mount_points) != 0:
                # We are only interested in the first mountpoint.
                mount_point = mount_points[0]
                mount_path = UDisksManager.bytes_to_path(mount_point)

                self._register_drive(block_device.IdUUID, mount_path, DriveType.NO_ACTION)
            else:
                LOGGER.warning(
                    f"No mountpoints available for {disk_bus_path}",
                )
        else:
            LOGGER.warning("No information on drive available. Aborting.")

    def _handle_cleanup_event(self, _: Dict[str, str]) -> None:
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

    def detect_initial_drives(self) -> None:
        """Detect and register drives as startup."""
        logging.info("Checking for initial drives at startup.")
        udisks = self.bus.get(".UDisks2")
        managed_objects = udisks.GetManagedObjects()
        block_devices = {
            x: managed_objects[x]
            for x in managed_objects.keys()
            if x.startswith("/org/freedesktop/UDisks2/block_devices/")
        }
        for path, data in block_devices.items():
            logging.debug(f"Checking drive at {path}")
            if 'org.freedesktop.UDisks2.Filesystem' in data.keys():
                filesystem = data['org.freedesktop.UDisks2.Filesystem']
                if 'MountPoints' in filesystem.keys():
                    mountpoints = filesystem['MountPoints']
                    if len(mountpoints) > 0:
                        mount_point = UDisksManager.bytes_to_path(
                            mountpoints[0],
                        )
                        if 'org.freedesktop.UDisks2.Block' in data.keys():
                            block = data['org.freedesktop.UDisks2.Block']
                            if 'IdUUID' in block.keys():
                                self._register_drive(block["IdUUID"], mount_point, DriveType.NO_ACTION)

    def _register_drive(self, uuid: str, mount_path: Path, drive_type: DriveType):
        """Register a drive with the controller."""
        if mount_path.exists():
            drive = Drive(
                uuid=uuid,
                mount_path=mount_path,
                drive_type=drive_type,
            )
            with self.controller.data_lock:
                LOGGER.info(f"Drive {drive.uuid} mounted ({drive_type.name}): {drive.mount_path}")
                self.controller.drive_group[drive.uuid] = drive
        else:
            LOGGER.warning(f"Unreadable drive mounted: {mount_path}")
