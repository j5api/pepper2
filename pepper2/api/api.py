"""Classes to interact with the pepper2 API."""

from typing import TYPE_CHECKING, Dict

from gi.repository import GLib
from pydbus import SystemBus

from pepper2.api.error import Pepper2Exception
from pepper2.common.daemon_status import DaemonStatus
from pepper2.daemon.dbus.drive import Drive

if TYPE_CHECKING:
    from pepper2.daemon.dbus.controller import Controller


class Pepper2:
    """Class to interact with pepper2 daemon."""

    def __init__(
        self,
        *,
        dbus_path: str = "uk.org.j5.pepper2",
    ) -> None:
        self._dbus_path = dbus_path

        self._connect()

    def _connect(self) -> None:
        """Connect to DBus."""
        try:
            self._bus = SystemBus()
        except GLib.Error as e:
            raise Pepper2Exception("Unable to connect to system bus.") from e

        try:
            self._controller: Controller = self._bus.get(self._dbus_path)
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
    def drives(self) -> Dict[str, Drive]:
        """
        Get information about detected drives.

        This method could definitely be made more efficient.
        """
        try:
            drive_list = self._controller.get_drive_list()
        except GLib.Error as e:
            raise Pepper2Exception("Error fetching drive list from daemon.") from e

        return {uuid: self.get_drive(uuid) for uuid in drive_list}

    def get_drive(self, uuid: str) -> Drive:
        """Get a drive."""
        bus_id = uuid.replace('-', '_')
        return Drive.from_proxy(self._bus.get("uk.org.j5.pepper2", bus_id))

    def kill_usercode(self) -> None:
        """Kill the currently running usercode."""
        if self.daemon_status is not DaemonStatus.CODE_RUNNING:
            raise ValueError("No usercode is running.")

        try:
            result = self._controller.kill_usercode()
        except GLib.Error as e:
            raise Pepper2Exception(
                "Error when sending kill usercode command.",
            ) from e

        if not result:
            raise Pepper2Exception("Unable to kill usercode.")

    def start_usercode(self) -> None:
        """Start any dead usercode."""
        if self.daemon_status in [DaemonStatus.CODE_RUNNING, DaemonStatus.CODE_STARTING]:
            raise ValueError("Usercode is already running.")

        if self.daemon_status in [DaemonStatus.READY, DaemonStatus.STARTING]:
            raise ValueError("There are no viable usercode drives available.")

        try:
            result = self._controller.start_usercode()
        except GLib.Error as e:
            raise Pepper2Exception(
                "Error when sending start usercode command.",
            ) from e

        if not result:
            raise Pepper2Exception("Unable to start usercode.")

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
