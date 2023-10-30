"""Pytest module for testing the rest client."""
import pytest

from pypaca.rest.rest import RestClient


def test_rest_client():
    """Test the rest client abstract base class."""
    with pytest.raises(TypeError):
        RestClient()
