"""Test that the pepper2 imports as expected."""

import pepper2


def test_module() -> None:
    """Test that the module behaves as expected."""
    assert pepper2.__version__ is not None
