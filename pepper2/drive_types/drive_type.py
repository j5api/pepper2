"""Drive Type."""
from abc import ABCMeta, abstractmethod

from pepper2.constraint import Constraint


class DriveType(metaclass=ABCMeta):
    """
    The Drive Type.

    A drive type defines all of the behaviour of a specific drive.
    This includes:

    - Matching the drive
    - Special actions of the drive.
    """

    name: str = "Unknown Drive"

    @classmethod
    @abstractmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        raise NotImplementedError

    # NO_ACTION = 0
    # USERCODE = 1
    # METADATA = 2
    # SYSTEM_UPDATE = 3
