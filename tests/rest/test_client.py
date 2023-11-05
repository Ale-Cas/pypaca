"""Test REST client."""

import pytest

from pypaca.rest.enums import BaseURL
from pypaca.rest.rest import RestClient


def test_client_initialization() -> None:
    """Test RestClient initialization."""
    with pytest.raises(
        ValueError, match="Either an oauth_token or an api_key may be supplied, but not both"
    ):
        RestClient(base_url=BaseURL.TRADING_PAPER, api_key="test", oauth_token="test")
    with pytest.raises(ValueError, match="You must provide both the `api_key` and `secret_key`"):
        RestClient(base_url=BaseURL.TRADING_PAPER, api_key="test")
    client = RestClient(base_url=BaseURL.TRADING_PAPER, api_key="test", secret_key="test")
    assert client._api_key == "test"
    assert client._secret_key == "test"
    assert isinstance(client._retry, int)
    assert isinstance(client._retry_wait, int)
    assert isinstance(client._retry_codes, tuple)
