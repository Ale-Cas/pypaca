"""Configuration for tests."""
from functools import lru_cache

import pytest

from pypaca import Credentials, TradingClient


@pytest.fixture(scope="package")
def vcr_config(record_mode: str = "once"):
    """Cassettes config.

    Params
    ------
    record_mode:
        - "rewrite": rewrite all cassettes if they have changed.
        - "none": only replay cassettes or throw an error if they are missing.
        - "once": record if there is no cassette, and if there is one replay it.
    """
    return {
        "decode_compressed_response": True,
        "record_mode": record_mode,
        "filter_headers": [
            ("APCA-API-KEY-ID", "SECRET"),
            ("APCA-API-SECRET-KEY", "SECRET"),
        ],
    }


@pytest.fixture(scope="package")
@lru_cache
def credentials() -> Credentials:
    """Get API credentials based on the environment and cache it."""
    return Credentials(_env_file=".env")


@pytest.fixture(scope="package")
def trading_client(credentials: Credentials) -> TradingClient:
    """Trading client."""
    return TradingClient(
        api_key=credentials.api_key,
        secret_key=credentials.secret_key,
    )
