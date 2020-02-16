"""Test the Drive class."""
from pathlib import Path

from pepper2.common.drive import Drive
from pepper2.common.drive_types import NoActionDriveType


def test_drive_instantiation() -> None:
    """Test that we can instantiate the Drive class."""
    drive = Drive(
        uuid="UUID",
        mount_path=Path(),
        drive_type=NoActionDriveType,
    )

    assert isinstance(drive, Drive)
    assert drive.uuid == "UUID"
    assert drive.mount_path == Path()
    assert drive.drive_type is NoActionDriveType
