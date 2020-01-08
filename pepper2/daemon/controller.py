"""Pepperd Controller Service."""
import logging
from threading import Lock
from typing import List, Mapping, Optional, Tuple

from gi.repository import GLib
from pkg_resources import resource_string

from pepper2 import __version__
from pepper2.daemon_status import DaemonStatus
from pepper2.drive_types import DRIVE_TYPES
from pepper2.drives import DriveGroup
from pepper2.usercode_driver import CodeStatus, UserCodeDriver

LOGGER = logging.getLogger(__name__)

CODE_DAEMON_STATUS_MAPPING: Mapping[CodeStatus, DaemonStatus] = {
    CodeStatus.IDLE: DaemonStatus.CODE_IDLE,
    CodeStatus.RUNNING: DaemonStatus.CODE_RUNNING,
    CodeStatus.KILLED: DaemonStatus.CODE_KILLED,
    CodeStatus.FINISHED: DaemonStatus.CODE_FINISHED,
    CodeStatus.CRASHED: DaemonStatus.CODE_CRASHED,
}


class Controller:
    """Pepper2 DBUS controller."""

    dbus = resource_string(__name__, "controller.xml").decode('utf-8')

    def __init__(self, loop: GLib.MainLoop):
        self.loop = loop
        self.ready = False
        self.data_lock = Lock()

        with self.data_lock:
            self.drive_group: DriveGroup = {}
            self.usercode_driver: Optional[UserCodeDriver] = None

    @property
    def status(self) -> DaemonStatus:
        """Current status of the daemon."""
        with self.data_lock:
            if self.usercode_driver is None:
                if self.ready:
                    return DaemonStatus.READY
                else:
                    return DaemonStatus.STARTING
            else:
                code_status = self.usercode_driver.status
                try:
                    return CODE_DAEMON_STATUS_MAPPING[code_status]
                except KeyError as e:
                    raise RuntimeError(
                        "Unknown UsercodeDriver status.",
                    ) from e

    # DBus Methods

    @property
    def version(self) -> str:
        """Get the version of pepper2."""
        LOGGER.debug("Version number request over bus.")
        return __version__

    def get_status(self) -> str:
        """
        Get the status of pepper2.

        TODO: Get rid of this funciton
        """
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
            LOGGER.debug(f"Response: \"{drive.uuid}\" at {drive.mount_path}")
            return True,\
                drive.uuid,\
                str(drive.mount_path.absolute()),\
                DRIVE_TYPES.index(drive.drive_type)
        else:
            LOGGER.debug(f"Response:  No such drive \"{uuid}\"")
            return False, "", "", -1
