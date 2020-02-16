"""Main class for Pepper2 Daemon."""

from fastapi import FastAPI

from pepper2 import __version__


class PepperDaemon(FastAPI):
    """
    Main pepper2 daemon class.

    Based on FastAPI.

    State for the application is stored here, in memory.
    It should not be run with multiple threads.
    """

    def __init__(self) -> None:

        super().__init__(
            title="Pepper2 Daemon",
            description="Robot Control Daemon",
            version=__version__,
            redoc_url=None,
        )
