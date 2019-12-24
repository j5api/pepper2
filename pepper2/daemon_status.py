"""Daemon status enum."""

from enum import Enum


class DaemonStatus(str, Enum):
    """Daemon status enum."""

    STARTING = "starting"
    READY = "ready"
    STOPPING = "stopping"
