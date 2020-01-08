"""Base class for User Code Drivers."""

from abc import ABCMeta, abstractmethod
from enum import Enum

from pepper2.drives import Drive


class CodeStatus(Enum):
    """Status of the running code."""

    IDLE = 0
    RUNNING = 1
    KILLED = 2
    FINISHED = 3
    CRASHED = 4


class UserCodeDriver(metaclass=ABCMeta):
    """
    User Code Driver class.

    This class defines a set of functionality that must be
    implemented in a usercode driver.

    A usercode driver runs and manages some user code through a
    uniform interface. This allows us to execute usercode in a
    variety of formats and environments, depending on the kit.
    """

    drive: Drive
    _status: CodeStatus

    def __init__(self, drive: Drive):
        self.drive = drive
        self._status = CodeStatus.IDLE

    @abstractmethod
    def start_execution(self) -> None:
        """Start the execution of the code."""
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def stop_execution(self) -> None:
        """Stop the execution of the code."""
        raise NotImplementedError  # pragma: nocover

    @property
    def status(self) -> CodeStatus:
        """Get the status of the executing code."""
        return self._status

    @status.setter
    def status(self, status: CodeStatus) -> None:
        """Set the status of the executing code."""
        self._status = status
