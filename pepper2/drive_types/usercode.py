"""Usercode Drive Type."""

from pepper2.constraint import Constraint, FilePresentConstraint

from .drive_type import DriveType


class UserCodeDriveType(DriveType):
    """A drive with usercode."""

    name: str = "USERCODE"

    @classmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        return FilePresentConstraint("main.py")
