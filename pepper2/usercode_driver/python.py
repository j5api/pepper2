"""Python Usercode Driver."""

from pepper2.drives import Drive

from .usercode_driver import UserCodeDriver


class PythonDriver(UserCodeDriver):
    """Usercode driver to execute Python."""

    def __init__(self, drive: Drive):
        self.drive = drive

    def start_execution(self) -> None:
        """Start the execution of the code."""
        print("PythonDriver Started Execution")

    def stop_execution(self) -> None:
        """Stop the execution of the code."""
        print("PythonDriver Stopped Execution")
