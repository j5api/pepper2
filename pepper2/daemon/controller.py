"""Pepperd Controller Service."""

from gi.repository import GLib

from pepper2 import __version__


class Controller:  # noqa: D400 D205 D208
    """
        <node>
            <interface name='uk.org.j5.pepper2.Controller'>
                <method name='GetVersion'>
                    <arg type='s' name='version' direction='out'/>
                </method>
                <method name='GetStatus'>
                    <arg type='s' name='status' direction='out'/>
                </method>
            </interface>
        </node>
    """

    def __init__(self, loop: GLib.MainLoop):
        self.loop = loop

    def GetVersion(self) -> str:
        """Get the version of pepper2."""
        return __version__

    def GetStatus(self) -> str:
        """Get the status of pepper2."""
        return "Awaiting Code Injection Event"
