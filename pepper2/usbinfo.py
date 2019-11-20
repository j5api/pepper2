"""USBInfo class."""

from pathlib import Path


class USBInfo:
    """Represents Information about an inserted USB."""

    def __init__(
            self,
            *,
            dbus_job_path: str,
            dbus_fs_path: str,
            dbus_drive_path: str,
            mount_path: Path,
    ):
        self.dbus_job_path = dbus_job_path
        self.dbus_fs_path = dbus_fs_path
        self.dbus_drive_path = dbus_drive_path
        self.mount_path = mount_path
