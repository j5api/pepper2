"""Pepperd Controller Service."""
import logging

from gi.repository import GLib

from pepper2 import __version__

LOGGER = logging.getLogger(__name__)


class Controller:  # noqa: D400 D205 D208
    """
        <node>
            <interface name='uk.org.j5.pepper2.Controller'>
                <method name='get_version'>
                    <arg type='s' name='version' direction='out'/>
                </method>
                <method name='get_status'>
                    <arg type='s' name='status' direction='out'/>
                </method>
            </interface>
        </node>
    """

    def __init__(self, loop: GLib.MainLoop):
        self.loop = loop

    def get_version(self) -> str:
        """Get the version of pepper2."""
        LOGGER.debug("Version number request over bus.")
        return __version__

    def get_status(self) -> str:
        """Get the status of pepper2."""
        LOGGER.debug("Status request over bus.")
        return "Awaiting Code Injection Event"
