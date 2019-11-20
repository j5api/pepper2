"""
Pepper2.

Library to interaction with robot management daemon.
"""

from .api import Pepper2
from .error import Pepper2Exception

__all__ = [
    "__version__",
    "Pepper2",
    "Pepper2Exception",
]

__version__ = "0.1.0"
