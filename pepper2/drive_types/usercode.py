"""Usercode Drive Type."""

import logging
from typing import TYPE_CHECKING

from pepper2.constraint import Constraint, FilePresentConstraint
from pepper2.usercode_driver.python import PythonUnixProcessDriver

from .drive_type import DriveType

if TYPE_CHECKING:
    from pepper2.daemon.controller import Controller
    from pepper2.drives import Drive

LOGGER = logging.getLogger(__name__)


class UserCodeDriveType(DriveType):
    """A drive with usercode."""

    name: str = "USERCODE"

    @classmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        return FilePresentConstraint("main.py")

    @classmethod
    def mount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """Perform the mount action."""
        with daemon_controller.data_lock:
            if daemon_controller.usercode_driver is None:
                # TODO: Dynamically choose Usercode Driver
                LOGGER.info("Starting usercode process.")
                daemon_controller.usercode_driver = PythonUnixProcessDriver(drive)
                daemon_controller.usercode_driver.start_execution()
            else:
                LOGGER.info(
                    "Unable to start Usercode: A usercode process "
                    "is already running",
                )

    @classmethod
    def unmount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """Perform the unmount/remove action."""
        with daemon_controller.data_lock:
            if daemon_controller.usercode_driver is not None:
                if drive == daemon_controller.usercode_driver.drive:
                    LOGGER.info("Stopping usercode process.")
                    daemon_controller.usercode_driver.stop_execution()
                    daemon_controller.usercode_driver = None
                else:
                    LOGGER.info(
                        "No action taken as usercode process is"
                        "from another drive.",
                    )
            else:
                LOGGER.info(
                    "No action taken as there is no usercode process.",
                )
