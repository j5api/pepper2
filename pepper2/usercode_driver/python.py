"""Python Usercode Driver."""

import logging
from subprocess import Popen, DEVNULL, TimeoutExpired
from signal import SIGTERM, SIGKILL, SIGCHLD
from typing import Optional

from pepper2.drives import Drive

from .usercode_driver import UserCodeDriver

LOGGER = logging.getLogger(__name__)


class PythonDriver(UserCodeDriver):
    """
    Usercode driver to execute Python.

    TODO: Name this class something better.
    """

    process: Optional[Popen]

    def __init__(self, drive: Drive):
        self.drive = drive
        self.process = None

    def start_execution(self) -> None:
        """Start the execution of the code."""
        self.process = Popen(
            ["python3", "main.py"],
            stdin=DEVNULL,
            cwd=self.drive.mount_path,
            start_new_session=True,  # Put the process in a new process group
        )

        LOGGER.info(f"Usercode process started with pid {self.process.pid}")

    def stop_execution(self) -> None:
        """Stop the execution of the code."""
        LOGGER.info(f"Sent SIGTERM to pid {self.process.pid}")
        self.process.send_signal(SIGTERM)
        try:
            self.process.communicate(timeout=5)
        except TimeoutExpired:
            pass
        self.process.send_signal(SIGKILL)
