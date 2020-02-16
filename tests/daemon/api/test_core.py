"""Tests for core endpoints."""

from starlette.testclient import TestClient

from pepper2 import __version__
from pepper2.daemon.app import app

client = TestClient(app)


def test_version_endpoint() -> None:
    """Test that the version endpoint returns the version."""
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == __version__
