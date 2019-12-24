"""No Action Drive Type."""

from pepper2.constraint import Constraint, TrueConstraint

from .drive_type import DriveType


class NoActionDriveType(DriveType):
    """A drive for which we take no action."""

    name: str = "NO_ACTION"

    @classmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        return TrueConstraint()
