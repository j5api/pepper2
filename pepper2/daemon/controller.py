"""Pepperd Controller Service."""
import logging
from threading import Lock
from typing import List

from gi.repository import GLib

from pepper2 import __version__
from pepper2.status import DaemonStatus
from pepper2.usbinfo import USBInfo

LOGGER = logging.getLogger(__name__)


class Controller:  # noqa: D400 D205 D208
    """
        <!-- Daemon Controller -->
        <!-- All state should be stored on this class. -->
        <!-- This XML is read by pydbus. -->
        <node>
            <interface name='uk.org.j5.pepper2.Controller'>
                <method name='get_version'>
                    <arg type='s' name='version' direction='out'/>
                </method>
                <method name='get_status'>
                    <arg type='s' name='status' direction='out'/>
                </method>
                <method name='get_drive_statuses'>
                    <arg type='as' name='drives' direction='out'/>
                </method>
            </interface>
        </node>
    """

    def __init__(self, loop: GLib.MainLoop):
        self._status = DaemonStatus.STARTING
        self.loop = loop
        self.data_lock = Lock()

        with self.data_lock:
            self.usb_infos: List[USBInfo] = []

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

    def get_version(self) -> str:
        """Get the version of pepper2."""
        LOGGER.debug("Version number request over bus.")
        return __version__

    def get_status(self) -> str:
        """Get the status of pepper2."""
        LOGGER.debug("Status request over bus.")
        return str(self.status.value)

    def get_drive_statuses(self) -> List[str]:
        """Get the drive statuses."""
        statuses = []
        with self.data_lock:
            current_data = self.usb_infos
        for d in current_data:
            statuses.append(f"{d.mount_path}: Unknown")
        return statuses
