"""Metadata Drive Type."""

from pepper2.constraint import Constraint, FilePresentConstraint

from .drive_type import DriveType


class MetadataDriveType(DriveType):
    """A drive with metadata."""

    name: str = "METADATA"

    @classmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        return FilePresentConstraint("pepper2.json")
