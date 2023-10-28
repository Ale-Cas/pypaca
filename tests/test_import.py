"""Test pypaca."""

import pypaca


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(pypaca.__name__, str)
