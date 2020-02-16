"""Test daemon_version on the python API."""

from starlette.testclient import TestClient

from pepper2 import __version__
from pepper2.api import Pepper2
from pepper2.daemon.app import app

client = TestClient(app, base_url="http://localhost:7032")


def test_daemon_version() -> None:
    """Test that we can fetch the daemon version."""
    pepper2 = Pepper2(session=client)
    assert pepper2.daemon_version == __version__
