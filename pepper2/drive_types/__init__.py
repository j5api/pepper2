"""Drive Types."""

from typing import List, Type

from .drive_type import DriveType
from .no_action import NoActionDriveType
from .usercode import UserCodeDriveType

# List of drive types, in priority order.
# The first one that matches will be selected.
DRIVE_TYPES: List[Type[DriveType]] = [
    UserCodeDriveType,
    NoActionDriveType,
]

__all__ = [
    'DRIVE_TYPES',
    'DriveType',
    'NoActionDriveType',
    'UserCodeDriveType',
]
