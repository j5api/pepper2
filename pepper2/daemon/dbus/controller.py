"""Pepperd Controller Service."""
import logging
from threading import RLock
from typing import List, Mapping, Optional, Tuple

from gi.repository import GLib
from pkg_resources import resource_string
from pydbus.bus import Bus
from pydbus.generic import signal

from pepper2 import __version__
from pepper2.common.daemon_status import DaemonStatus
from pepper2.common.drive_types import DRIVE_TYPES
from pepper2.daemon.dbus.drive import DriveGroup
from pepper2.daemon.publishable_group import PublishableGroup
from pepper2.daemon.usercode_driver import CodeStatus, UserCodeDriver

LOGGER = logging.getLogger(__name__)

CODE_DAEMON_STATUS_MAPPING: Mapping[CodeStatus, DaemonStatus] = {
    CodeStatus.STARTING: DaemonStatus.CODE_STARTING,
    CodeStatus.RUNNING: DaemonStatus.CODE_RUNNING,
    CodeStatus.KILLED: DaemonStatus.CODE_KILLED,
    CodeStatus.FINISHED: DaemonStatus.CODE_FINISHED,
    CodeStatus.CRASHED: DaemonStatus.CODE_CRASHED,
}


class Controller:
    """Pepper2 DBUS controller."""

    dbus = resource_string(__name__, "controller.xml").decode('utf-8')

    PropertiesChanged = signal()

    def __init__(self, loop: GLib.MainLoop, bus: Bus):
        self.loop = loop
        self.bus = bus
        self.data_lock = RLock()

        with self.data_lock:
            self._daemon_status: DaemonStatus = DaemonStatus.STARTING
            self.drive_group: DriveGroup = PublishableGroup(bus, "Drive")
            self.usercode_driver: Optional[UserCodeDriver] = None

    @property
    def daemon_status(self) -> DaemonStatus:
        """Get the current daemon_status of the daemon."""
        with self.data_lock:
            return self._daemon_status

    @daemon_status.setter
    def daemon_status(self, daemon_status: DaemonStatus) -> None:
        """Set the current daemon_status of the daemon."""
        with self.data_lock:
            self._daemon_status = daemon_status
            self.PropertiesChanged(
                "uk.org.j5.pepper2.Controller",
                {"daemon_status": daemon_status},
                [],
            )

    @property
    def version(self) -> str:
        """Get the version of pepper2."""
        LOGGER.debug("Version number request over bus.")
        return __version__

    @property
    def usercode_drive(self) -> str:
        """
        Get the drive of the executing usercode.

        :returns: the uuid of the executing drive.
        """
        LOGGER.debug(f"Usercode drive uuid request over bus.")
        if self.usercode_driver is None:
            return ""
        else:
            return self.usercode_driver.drive.uuid

    @property
    def usercode_driver_name(self) -> str:
        """
        Get the usercode_driver of the executing usercode.

        :returns: the name of the driver
        """
        LOGGER.debug(f"Usercode Driver request over bus.")
        if self.usercode_driver is None:
            return ""
        else:
            return self.usercode_driver.__class__.__name__

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

    def kill_usercode(self) -> bool:
        """
        Kill any running usercode.

        :returns: Boolean of success.
        """
        LOGGER.debug(f"Usercode kill request over bus.")
        if self.usercode_driver is None or \
                self.usercode_driver.status is not CodeStatus.RUNNING:
            return False
        else:
            LOGGER.info("Killing Usercode.")
            self.usercode_driver.stop_execution()
            return True

    def start_usercode(self) -> bool:
        """
        Start any dead usercode.

        :returns: Boolean of success.
        """
        LOGGER.debug(f"Usercode start request over bus.")
        if self.usercode_driver is None or \
                self.usercode_driver.status is CodeStatus.RUNNING:
            return False
        else:
            LOGGER.info("Starting Usercode.")
            self.usercode_driver.start_execution()
            return True

    # Not exposed on interface.

    def inform_code_status(self, code_status: CodeStatus) -> None:
        """Inform daemon_controller of an updated code status."""
        try:
            self.daemon_status = CODE_DAEMON_STATUS_MAPPING[code_status]
        except KeyError as e:
            raise RuntimeError(
                "Unknown UsercodeDriver status.",
            ) from e
