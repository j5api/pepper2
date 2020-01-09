"""Python Usercode Driver."""

from typing import List

from .unix_process import UnixProcessDriver


class PythonUnixProcessDriver(UnixProcessDriver):
    """
    Usercode driver to execute Python.

    Executes as the current user in a separate unix process group.
    """

    def get_command(self) -> List[str]:
        """Get the command to execute."""
        return ["python3", "-u", "main.py"]
