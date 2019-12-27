"""Python Usercode Driver."""

import logging
from signal import SIGCHLD, SIGKILL, SIGTERM, Signals, getsignal, signal
from subprocess import DEVNULL, Popen, TimeoutExpired
from types import FrameType
from typing import TYPE_CHECKING, Optional

from pepper2.drives import Drive

from .usercode_driver import UserCodeDriver

if TYPE_CHECKING:
    # _HANDLER is only available in typeshed.
    from signal import _HANDLER


LOGGER = logging.getLogger(__name__)


class PythonDriver(UserCodeDriver):
    """
    Usercode driver to execute Python.

    TODO: Name this class something better.
    """

    _process: Optional[Popen]

    def __init__(self, drive: Drive):
        self.drive = drive
        self._process = None
        self._original_sigchld: _HANDLER = getsignal(SIGCHLD)

    def start_execution(self) -> None:
        """Start the execution of the code."""
        signal(SIGCHLD, self.sigchld_handler)
        self._process = Popen(
            ["python3", "main.py"],
            stdin=DEVNULL,
            cwd=self.drive.mount_path,
            start_new_session=True,  # Put the process in a new process group
        )

        LOGGER.info(f"Usercode process started with pid {self._process.pid}")

    def stop_execution(self) -> None:
        """Stop the execution of the code."""
        self._reset_sigchld()

        if self._process is not None:
            LOGGER.info(f"Sent SIGTERM to pid {self._process.pid}")
            self._process.send_signal(SIGTERM)
            try:
                self._process.communicate(timeout=5)
            except TimeoutExpired:
                pass
            self._process.send_signal(SIGKILL)
            self._process = None
        else:
            LOGGER.info("No usercode process to stop.")

    def sigchld_handler(self, _: Signals, __: FrameType) -> None:
        """
        Handler for SIGCHLD.

        This is called when the child process of this process dies.
        """
        self._reset_sigchld()

        if self._process is not None:
            return_code = self._process.poll()

            if return_code == 0:
                LOGGER.info("Usercode finished successfully.")
            else:
                LOGGER.info(
                    f"Usercode finished unsuccessfully (return code: {return_code}).",
                )
            self._process = None

    def _reset_sigchld(self) -> None:
        """Reset the SIGCHLD handler to the original."""
        signal(SIGCHLD, self._original_sigchld)
