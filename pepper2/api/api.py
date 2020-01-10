"""Classes to interact with the pepper2 API."""

from pathlib import Path
from typing import TYPE_CHECKING

from gi.repository import GLib
from pydbus import SystemBus

from pepper2.api.error import Pepper2Exception
from pepper2.common.daemon_status import DaemonStatus
from pepper2.common.drive_types import DRIVE_TYPES
from pepper2.common.drives import Drive, DriveGroup

if TYPE_CHECKING:
    from pepper2.daemon.controller import Controller


class Pepper2:
    """Class to interact with pepper2 daemon."""

    def __init__(
        self,
        *,
        controller_endpoint: str = "uk.org.j5.pepper2",
    ) -> None:
        self._controller_endpoint = controller_endpoint

        self._connect()

    def _connect(self) -> None:
        """Connect to DBus."""
        try:
            self._bus = SystemBus()
        except GLib.Error as e:
            raise Pepper2Exception("Unable to connect to system bus.") from e

        try:
            self._controller: Controller = self._bus.get(self._controller_endpoint)
        except GLib.Error as e:
            raise Pepper2Exception("Unable to find daemon on bus.") from e

    @property
    def daemon_version(self) -> str:
        """Get the daemon version."""
        try:
            return self._controller.version
        except GLib.Error as e:
            raise Pepper2Exception("Error fetching version from daemon.") from e

    @property
    def daemon_status(self) -> DaemonStatus:
        """Get the daemon status."""
        try:
            status_string = self._controller.daemon_status
        except GLib.Error as e:
            raise Pepper2Exception("Error fetching status from daemon.") from e

        try:
            return DaemonStatus(status_string)
        except ValueError:
            raise Pepper2Exception(
                f"Received unknown status string from daemon: {status_string}",
            )

    @property
    def drives(self) -> DriveGroup:
        """
        Get information about detected drives.

        This method could definitely be made more efficient.
        """
        try:
            drive_list = self._controller.get_drive_list()
        except GLib.Error as e:
            raise Pepper2Exception("Error fetching drive list from daemon.") from e

        return {drive_uuid: self.get_drive(drive_uuid) for drive_uuid in drive_list}

    def get_drive(self, uuid: str) -> Drive:
        """Get a drive by uuid."""
        try:
            raw_data = self._controller.get_drive(uuid)
        except GLib.Error as e:
            raise Pepper2Exception("Error fetching drive data from daemon.") from e

        if raw_data[0] == -1:
            raise ValueError(f"No such drive {uuid}")

        try:
            drive_type = DRIVE_TYPES[raw_data[3]]
        except IndexError as e:
            raise Pepper2Exception("Unknown drive type code.") from e

        return Drive(
            uuid=raw_data[1],
            mount_path=Path(raw_data[2]),
            drive_type=drive_type,
        )

    @property
    def usercode_drive(self) -> Drive:
        """
        Get the drive of the executing usercode.

        :returns: the executing drive.
        """
        try:
            uuid = self._controller.usercode_drive
        except GLib.Error as e:
            raise Pepper2Exception("Error fetching drive list from daemon.") from e

        if uuid == "":
            raise ValueError("No usercode is currently executing")
        else:
            return self.get_drive(uuid)

    @property
    def usercode_driver_name(self) -> str:
        """Get the usercode driver name."""
        try:
            name = self._controller.usercode_driver_name
        except GLib.Error as e:
            raise Pepper2Exception("Error fetching drive list from daemon.") from e

        if name == "":
            raise ValueError("No usercode is currently executing")
        else:
            return name
