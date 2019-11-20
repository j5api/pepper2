"""Classes to interact with the pepper2 API."""

from gi.repository import GLib
from pydbus import SystemBus

from .error import Pepper2Exception
from .status import DaemonStatus


class Pepper2:

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
            self._controller = self._bus.get(self._controller_endpoint)
        except GLib.Error as e:
            raise Pepper2Exception("Unable to find daemon on bus.") from e

    @property
    def daemon_version(self) -> str:
        """Get the daemon version."""
        try:
            return self._controller.get_version()
        except GLib.Error as e:
            raise Pepper2Exception("Error fetching version from daemon.") from e

    @property
    def daemon_status(self) -> DaemonStatus:
        """Get the daemon status."""
        try:
            status_string = self._controller.get_status()
        except GLib.Error as e:
            raise Pepper2Exception("Error fetching status from daemon.") from e

        try:
            return DaemonStatus(status_string)
        except ValueError:
            raise Pepper2Exception(
                f"Received unknown status string from daemon: {status_string}",
            )
