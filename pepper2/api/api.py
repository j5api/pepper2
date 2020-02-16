"""Classes to interact with the pepper2 API."""

from typing import Dict

from pepper2.common.daemon_status import DaemonStatus
from pepper2.common.drive import Drive


class Pepper2:
    """Class to interact with pepper2 daemon."""

    @property
    def daemon_version(self) -> str:
        """Get the daemon version."""
        raise NotImplementedError("Cannot fetch daemon version")

    @property
    def daemon_status(self) -> DaemonStatus:
        """Get the daemon status."""
        raise NotImplementedError("Cannot fetch daemon status.")

    @property
    def drives(self) -> Dict[str, Drive]:
        """Get information about detected drives."""
        raise NotImplementedError("Cannot fetch drive information.")

    def kill_usercode(self) -> None:
        """Kill the currently running usercode."""
        raise NotImplementedError("Cannot kill usercode.")

    def start_usercode(self) -> None:
        """Start any dead usercode."""
        raise NotImplementedError("Cannot start usercode.")

    @property
    def usercode_drive(self) -> Drive:
        """
        Get the drive of the executing usercode.

        :returns: the executing drive.
        """
        raise NotImplementedError("Cannot fetch usercode drive.")

    @property
    def usercode_driver_name(self) -> str:
        """Get the usercode driver name."""
        raise NotImplementedError("Cannot fetch usercode driver name.")
