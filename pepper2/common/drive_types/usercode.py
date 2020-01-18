"""Usercode Drive Type."""

import logging
from typing import TYPE_CHECKING, Mapping, Type

from pepper2.common.constraint import (
    Constraint,
    FalseConstraint,
    FilePresentConstraint,
    OrConstraint,
)
from pepper2.common.daemon_status import DaemonStatus
from pepper2.daemon.usercode_driver import (
    PythonUnixProcessDriver,
    UserCodeDriver,
)

from .drive_type import DriveType
from .no_action import NoActionDriveType

if TYPE_CHECKING:
    from pepper2.daemon.dbus.controller import Controller
    from pepper2.daemon.dbus.drive import Drive

LOGGER = logging.getLogger(__name__)

DRIVERS: Mapping[str, Type[UserCodeDriver]] = {
    "main.py": PythonUnixProcessDriver,
}


class UserCodeDriveType(DriveType):
    """A drive with usercode."""

    name: str = "USERCODE"

    @classmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        constraint: Constraint = FalseConstraint()

        for filename in DRIVERS.keys():
            constraint = OrConstraint(constraint, FilePresentConstraint(filename))

        return constraint

    @classmethod
    def mount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """Perform the mount action."""
        with daemon_controller.data_lock:
            if daemon_controller.usercode_driver is None:
                for filename in DRIVERS.keys():
                    if drive.mount_path.joinpath(filename).exists():
                        driver = DRIVERS[filename]
                        LOGGER.info(
                            f"Starting usercode process with {driver.__name__}.",
                        )
                        daemon_controller.usercode_driver = driver(
                            drive,
                            daemon_controller,
                        )
                        daemon_controller.usercode_driver.start_execution()
                        return None
                LOGGER.error(
                    "Unable to start Usercode: Unable to find "
                    "driver for filename.",
                )
            else:
                LOGGER.info(
                    "Unable to start Usercode: A usercode process "
                    "is already running",
                )

                # Change drive type so that this usercode does not get executed.
                LOGGER.debug(
                    f"Changing drive type of {drive.uuid} to NoActionDriveType",
                )
                drive.drive_type = NoActionDriveType

    @classmethod
    def unmount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """Perform the unmount/remove action."""
        with daemon_controller.data_lock:
            if daemon_controller.usercode_driver is not None:
                if drive == daemon_controller.usercode_driver.drive:
                    LOGGER.info("Stopping usercode process.")
                    daemon_controller.usercode_driver.stop_execution()
                    daemon_controller.usercode_driver = None
                    daemon_controller.daemon_status = DaemonStatus.READY
                else:
                    LOGGER.info(
                        "No action taken as usercode process is"
                        "from another drive.",
                    )
            else:
                LOGGER.info(
                    "No action taken as there is no usercode process.",
                )
