"""Pepperd Controller Service."""
import logging
from threading import Lock
from typing import List, Tuple

from gi.repository import GLib
from pkg_resources import resource_string

from pepper2 import __version__
from pepper2.drives import DriveGroup
from pepper2.status import DaemonStatus

LOGGER = logging.getLogger(__name__)


class Controller:
    """Pepper2 DBUS controller."""

    dbus = resource_string(__name__, "controller.xml").decode('utf-8')

    def __init__(self, loop: GLib.MainLoop):
        self._status = DaemonStatus.STARTING
        self.loop = loop
        self.data_lock = Lock()

        with self.data_lock:
            self.drive_group: DriveGroup = {}

    @property
    def status(self) -> DaemonStatus:
        """Current status of the daemon."""
        with self.data_lock:
            return self._status

    @status.setter
    def status(self, status: DaemonStatus) -> None:
        """Current status of the daemon."""
        with self.data_lock:
            self._status = status

    # DBus Methods

    @property
    def version(self) -> str:
        """Get the version of pepper2."""
        LOGGER.debug("Version number request over bus.")
        return __version__

    def get_status(self) -> str:
        """Get the status of pepper2."""
        LOGGER.debug("Status request over bus.")
        return str(self.status.value)

    def get_drive_list(self) -> List[str]:
        """Get a list of drives."""
        LOGGER.debug("Drive list request over bus.")
        return [x for x in self.drive_group.keys()]

    def get_drive(self, uuid: str) -> Tuple[bool, str, str, int]:
        """
        Get an individual drive.

        :returns Tuple of (success, uuid, mount_path, type_id)
        """
        LOGGER.debug(f"Drive info request for \"{uuid}\" over bus.")
        if uuid in self.drive_group.keys():
            drive = self.drive_group[uuid]
            LOGGER.debug(f"Found drive \"{drive.uuid}\" at {drive.mount_path}")
            return True,\
                drive.uuid,\
                str(drive.mount_path.absolute()),\
                drive.drive_type.value
        else:
            LOGGER.debug(f"No such drive \"{uuid}\"")
            return False, "", "", -1
