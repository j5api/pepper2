"""Base class for User Code Drivers."""

from abc import ABCMeta, abstractmethod

from pepper2.drives import Drive


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

    @abstractmethod
    def start_execution(self) -> None:
        """Start the execution of the code."""
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def stop_execution(self) -> None:
        """Stop the execution of the code."""
        raise NotImplementedError  # pragma: nocover
