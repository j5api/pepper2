"""Classes to interact with the pepper2 API."""

from pydbus import SystemBus

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
        self._bus = SystemBus()
        self._controller = self._bus.get(self._controller_endpoint)

    @property
    def daemon_version(self) -> str:
        """Get the daemon version."""
        return self._controller.get_version()

    @property
    def daemon_status(self) -> DaemonStatus:
        """Get the daemon status."""
        status_string = self._controller.get_status()
        return DaemonStatus(status_string)
