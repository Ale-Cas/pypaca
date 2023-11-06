"""Test TradingClient class."""
from uuid import UUID

import pytest

from pypaca import TradingClient
from pypaca.trading.enums import TradeConfirmationEmail
from pypaca.trading.models import AccountConfiguration, Order, TradeAccount
from pypaca.trading.requests import (
    CancelOrderResponse,
    OrderRequest,
    PatchAccountConfiguration,
)


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


@pytest.mark.vcr()
def test_submit_order(trading_client: TradingClient) -> None:
    """Test TradingClient submit_order method."""
    symbol = "AAPL"
    qty = 1
    side = "buy"
    type_ = "market"
    time_in_force = "day"
    order = trading_client.submit_order(
        OrderRequest(
            symbol=symbol,
            qty=qty,
            side=side,
            type=type_,
            time_in_force=time_in_force,
        )
    )
    assert isinstance(order, Order)
    assert order.symbol == symbol
    assert order.qty == qty
    assert order.side == side
    assert order.order_type == type_
    assert order.time_in_force == time_in_force


@pytest.mark.vcr()
def test_get_orders(trading_client: TradingClient) -> None:
    """Test TradingClient get_orders method."""
    orders = trading_client.get_orders()
    assert isinstance(orders, list)
    assert all(isinstance(order, Order) for order in orders)


@pytest.mark.vcr()
def test_get_order_by_id(trading_client: TradingClient) -> None:
    """Test TradingClient get_order_by_id method."""
    order_id = UUID("fa50db58-1c8e-4437-b7ba-2a7bf839f522")
    order = trading_client.get_order_by_id(order_id)
    assert isinstance(order, Order)
    assert order.id_ == order_id


@pytest.mark.vcr()
def test_get_order_by_client_id(trading_client: TradingClient) -> None:
    """Test TradingClient get_order_by_client_id method."""
    client_order_id = "037716b9-4c2f-4ce3-b15e-3947e810aa2a"
    order = trading_client.get_order_by_client_id(client_order_id)
    assert isinstance(order, Order)
    assert order.client_order_id == client_order_id


@pytest.mark.vcr()
def test_cancel_orders(trading_client: TradingClient) -> None:
    """Test TradingClient cancel_orders method."""
    cancel_responses = trading_client.cancel_orders()
    assert isinstance(cancel_responses, list)
    assert all(isinstance(response, CancelOrderResponse) for response in cancel_responses)


@pytest.mark.vcr()
def test_cancel_order_by_id(trading_client: TradingClient) -> None:
    """Test TradingClient cancel_order_by_id method."""
    order_id = UUID("fa50db58-1c8e-4437-b7ba-2a7bf839f522")
    trading_client.cancel_order_by_id(order_id)
