"""Daemon status enum."""

from enum import Enum


class DaemonStatus(str, Enum):
    """Daemon status enum."""

    STARTING = "starting"
    READY = "ready"
    CODE_RUNNING = "code_running"
    CODE_FINISHED = "code_stopped"
    CODE_CRASHED = "code_crashed"
