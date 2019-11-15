"""
Udisks2 Controller.

Abstract and talk to UDisks.
"""
import logging
from pathlib import Path
from time import sleep
from typing import Dict

from pydbus.bus import Bus

from .controller import Controller
from .usbinfo import USBInfo

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
                        self.handle_mount_event(path, event_data)

                    if event_data["Operation"] == "cleanup":
                        LOGGER.info(f"Removal Event detected at {path}")
                        sleep(0.3)
                        self.handle_cleanup_event(path, event_data)

    def handle_mount_event(self, path: str, event_data: Dict[str, str]) -> None:
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
                    LOGGER.info(f"Drive mounted: {mount_path}")
                    usb_info = USBInfo(
                        dbus_job_path=path,
                        dbus_fs_path=disk_bus_path,
                        dbus_drive_path=block_device.Drive,
                        mount_path=mount_path,
                    )
                    with self.controller.data_lock:
                        self.controller.usb_infos.append(usb_info)
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

    def handle_cleanup_event(self, path: str, event_data: Dict[str, str]) -> None:
        """Handle a cleanup event."""
        with self.controller.data_lock:
            # We have no information to tell which drive left.
            # Thus we need to check.
            updated_info = []
            for drive in self.controller.usb_infos:
                if drive.mount_path.exists():
                    updated_info.append(drive)
                else:
                    LOGGER.info(f"Drive removed: {drive.mount_path}")
            self.controller.usb_infos = updated_info
