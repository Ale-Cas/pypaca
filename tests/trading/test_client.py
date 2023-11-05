"""Test REST client."""

import pytest

from pypaca import TradingClient
from pypaca.trading.enums import TradeConfirmationEmail
from pypaca.trading.models import AccountConfiguration, TradeAccount
from pypaca.trading.requests import PatchAccountConfiguration


@pytest.mark.vcr()
def test_get_account(trading_client: TradingClient) -> None:
    """Test TradingClient get_account method."""
    account = trading_client.get_account()
    assert isinstance(account, TradeAccount)


@pytest.mark.vcr()
def test_get_account_configurations(trading_client: TradingClient) -> None:
    """Test TradingClient get_account_configurations method."""
    account_config = trading_client.get_account_configurations()
    assert isinstance(account_config, AccountConfiguration)


@pytest.mark.vcr()
def test_set_account_configurations(trading_client: TradingClient) -> None:
    """Test TradingClient set_account_configurations method."""
    _trade_confirm_email = TradeConfirmationEmail.NONE
    account_config = trading_client.set_account_configurations(
        PatchAccountConfiguration(fractional_trading=True, trade_confirm_email=_trade_confirm_email)
    )
    assert isinstance(account_config, AccountConfiguration)
    assert account_config.fractional_trading
    assert account_config.trade_confirm_email == _trade_confirm_email
