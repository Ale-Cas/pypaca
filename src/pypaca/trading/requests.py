"""Requests models."""
from datetime import date, datetime, timedelta
from typing import Any

import pandas as pd
from pydantic import Field, model_validator

from pypaca.rest import Sort
from pypaca.rest.models import ModelWithID
from pypaca.rest.requests import NonEmptyRequest
from pypaca.trading.enums import (
    AssetClass,
    AssetExchange,
    AssetStatus,
    CorporateActionDateType,
    CorporateActionType,
    DTBPCheck,
    OrderClass,
    OrderSide,
    OrderType,
    PDTCheck,
    QueryOrderStatus,
    TimeInForce,
    TradeConfirmationEmail,
)


class PatchAccountConfiguration(NonEmptyRequest):
    """
    Represents configuration options for a TradeAccount.

    Attributes
    ----------
        dtbp_check (DTBPCheck): Day Trade Buying Power Check. Controls Day Trading Margin Call (DTMC) checks.
        fractional_trading (bool): If true, account is able to participate in fractional trading
        max_margin_multiplier (str): A number between 1-4 that represents your max margin multiplier
        no_shorting (bool): If true then Account becomes long-only mode.
        pdt_check (PDTCheck): Controls Pattern Day Trader (PDT) checks.
        suspend_trade (bool): If true Account becomes unable to submit new orders
        trade_confirm_email (TradeConfirmationEmail): Controls whether Trade confirmation emails are sent.
        ptp_no_exception_entry (bool): If set to true then Alpaca will accept orders for PTP symbols with no exception. Default is false.
    """

    dtbp_check: DTBPCheck | None = None
    fractional_trading: bool | None = None
    max_margin_multiplier: str | None = None
    no_shorting: bool | None = None
    pdt_check: PDTCheck | None = None
    suspend_trade: bool | None = None
    trade_confirm_email: TradeConfirmationEmail | None = None
    ptp_no_exception_entry: bool | None = None


class ClosePositionRequest(NonEmptyRequest):
    """
    Used for providing details for closing a position.

    Attributes
    ----------
        qty (str): The number of shares to liquidate.
        percentage (str): The percentage of shares to liquidate.
    """

    qty: str | None = None
    percentage: str | None = None

    @model_validator(mode="before")
    @classmethod
    def root_validator(cls, values: dict) -> dict:
        """Validate that qty or percentage is set, but not both."""
        qty = values.get("qty", None)
        percentage = values.get("percentage", None)
        if qty is None and percentage is None:
            raise ValueError(
                "qty or percentage must be given to the ClosePositionRequest, got None for both."
            )

        if qty is not None and percentage is not None:
            raise ValueError(
                "Only one of qty or percentage must be given to the ClosePositionRequest, got both."
            )

        return values


class GetPortfolioHistoryRequest(NonEmptyRequest):
    """
    Represents the optional filtering you can do when requesting a PortfolioHistory object.

    Attributes
    ----------
        period (Optional[str]): The duration of the data in number + unit, such as 1D. unit can be D for day, W for
          week, M for month and A for year. Defaults to 1M.
        timeframe (Optional[str]): The resolution of time window. 1Min, 5Min, 15Min, 1H, or 1D. If omitted, 1Min for
          less than 7 days period, 15Min for less than 30 days, or otherwise 1D.
        date_end (Optional[date]): The date the data is returned up to. Defaults to the current market date (rolls over
          at the market open if extended_hours is false, otherwise at 7am ET).
        extended_hours (Optional[bool]): If true, include extended hours in the result. This is effective only for
          timeframe less than 1D.
    """

    period: str | None = None
    timeframe: str | None = None
    date_end: date | None = None
    extended_hours: bool | None = None


class GetCalendarRequest(NonEmptyRequest):
    """Represents the optional filtering you can do when requesting a Calendar object."""

    start: date | None = None
    end: date | None = None


class CreateWatchlistRequest(NonEmptyRequest):
    """
    Represents the fields you can specify when creating a Watchlist.

    Attributes
    ----------
        name(str): Name of the Watchlist
        symbols(List[str]): Symbols of Assets to watch
    """

    name: str
    symbols: list[str]


class UpdateWatchlistRequest(NonEmptyRequest):
    """
    Represents the fields you can specify when updating a Watchlist.

    Attributes
    ----------
        name(Optional[str]): Name of the Watchlist
        symbols(Optional[List[str]]): Symbols of Assets to watch
    """

    name: str | None = None
    symbols: list[str] | None = None

    @model_validator(mode="before")
    @classmethod
    def root_validator(cls, values: dict) -> dict:
        """Validate that name or symbols is set, but not both."""
        if ("name" not in values or values["name"] is None) and (
            "symbols" not in values or values["symbols"] is None
        ):
            raise ValueError("One of 'name' or 'symbols' must be defined")

        return values


class GetAssetsRequest(NonEmptyRequest):
    """
    When querying for available assets, this model provides the parameters that can be filtered by.

    Attributes
    ----------
        status (Optional[AssetStatus]): The active status of the asset.
        asset_class (Optional[AssetClass]): The type of asset (i.e. us_equity, crypto).
        exchange (Optional[AssetExchange]): The exchange the asset trades on.
        attributes (Optional[str]): Comma separated values to query for more than one attribute.
    """

    status: AssetStatus | None = None
    asset_class: AssetClass | None = None
    exchange: AssetExchange | None = None


class TakeProfitRequest(NonEmptyRequest):
    """
    Used for providing take profit details for a bracket order.

    Attributes
    ----------
        limit_price (float): The execution price for exiting a profitable trade.
    """

    limit_price: float


class StopLossRequest(NonEmptyRequest):
    """
    Used for providing stop loss details for a bracket order.

    Attributes
    ----------
        stop_price (float): The price at which the stop loss is triggered.
        limit_price (Optional[float]): The execution price for exiting a losing trade. If not provided, the
            stop loss will execute as a market order.
    """

    stop_price: float
    limit_price: float | None = None


class GetOrdersRequest(NonEmptyRequest):
    """Contains data for submitting a request to retrieve orders.

    Attributes
    ----------
        status (Optional[QueryOrderStatus]): Order status to be queried. open, closed or all. Defaults to open. Not same as OrderStatus property of Order.
        limit (Optional[int]): The maximum number of orders in response. Defaults to 50 and max is 500.
        after (Optional[datetime]): The response will include only ones submitted after this timestamp.
        until (Optional[datetime]): The response will include only ones submitted until this timestamp.
        direction (Optional[Sort]): The chronological order of response based on the submission time. asc or desc. Defaults to desc.
        nested (Optional[bool]): If true, the result will roll up multi-leg orders under the legs field of primary order.
        side (Optional[OrderSide]): Filters down to orders that have a matching side field set.
        symbols (Optional[List[str]]): List of symbols to filter by.
    """

    status: QueryOrderStatus | None = None
    limit: int | None = None  # not pagination = None
    after: datetime | None = None
    until: datetime | None = None
    direction: Sort | None = None
    nested: bool | None = None
    side: OrderSide | None = None
    symbols: list[str] | None = None


class GetOrderByIdRequest(NonEmptyRequest):
    """Contains data for submitting a request to retrieve a single order by its order id.

    Attributes
    ----------
        nested (bool): If true, the result will roll up multi-leg orders under the legs field of primary order.
    """

    nested: bool


class ReplaceOrderRequest(NonEmptyRequest):
    """Contains data for submitting a request to replace an order.

    Attributes
    ----------
        qty (Optional[int]): Number of shares to trade
        time_in_force (Optional[TimeInForce]): The new expiration logic of the order.
        limit_price (Optional[float]): Required if type of order being replaced is limit or stop_limit
        stop_price (Optional[float]): Required if type of order being replaced is stop or stop_limit
        trail (Optional[float]): The new value of the trail_price or trail_percent value (works only for type=“trailing_stop”)
        client_order_id (Optional[str]): A unique identifier for the order.
    """

    qty: int | None = None
    time_in_force: TimeInForce | None = None
    limit_price: float | None = None
    stop_price: float | None = None
    trail: float | None = None
    client_order_id: str | None = None


class CancelOrderResponse(ModelWithID):
    """
    Data returned after requesting to cancel an order. It contains the cancel status of an order.

    Attributes
    ----------
        id (UUID): The order id
        status (int): The HTTP status returned after attempting to cancel the order.
    """

    status: int


class OrderRequest(NonEmptyRequest):
    """
    Base class for requests for creating an order.

    You probably shouldn't directly use
    this class when submitting an order. Instead, use one of the order type specific classes.

    Attributes
    ----------
        symbol (str): The symbol identifier for the asset being traded
        qty (Optional[float]): The number of shares to trade. Fractional qty for stocks only with market orders.
        notional (Optional[float]): The base currency value of the shares to trade. For stocks, only works with MarketOrders.
            **Does not work with qty**.
        side (OrderSide): Whether the order will buy or sell the asset.
        type (OrderType): The execution logic type of the order (market, limit, etc).
        time_in_force (TimeInForce): The expiration logic of the order.
        extended_hours (Optional[float]): Whether the order can be executed during regular market hours.
        client_order_id (Optional[str]): A string to identify which client submitted the order.
        order_class (Optional[OrderClass]): The class of the order. Simple orders have no other legs.
        take_profit (Optional[TakeProfitRequest]): For orders with multiple legs, an order to exit a profitable trade.
        stop_loss (Optional[StopLossRequest]): For orders with multiple legs, an order to exit a losing trade.
    """

    symbol: str
    qty: float | None = None
    notional: float | None = None
    side: OrderSide
    type_: OrderType = Field(..., alias="type")
    time_in_force: TimeInForce
    order_class: OrderClass | None = None
    extended_hours: bool | None = None
    client_order_id: str | None = None
    take_profit: TakeProfitRequest | None = None
    stop_loss: StopLossRequest | None = None

    @model_validator(mode="before")
    @classmethod
    def root_validator(cls, values: dict) -> dict:
        """Validate that qty or notional is set, but not both."""
        qty_set = "qty" in values and values["qty"] is not None
        notional_set = "notional" in values and values["notional"] is not None

        if not qty_set and not notional_set:
            raise ValueError("At least one of qty or notional must be provided")
        if qty_set and notional_set:
            raise ValueError("Both qty and notional can not be set.")

        return values


class MarketOrderRequest(OrderRequest):
    """
    Used to submit a market order.

    Attributes
    ----------
        symbol (str): The symbol identifier for the asset being traded
        qty (Optional[float]): The number of shares to trade. Fractional qty for stocks only with market orders.
        notional (Optional[float]): The base currency value of the shares to trade. For stocks, only works with MarketOrders.
            **Does not work with qty**.
        side (OrderSide): Whether the order will buy or sell the asset.
        type (OrderType): The execution logic type of the order (market, limit, etc).
        time_in_force (TimeInForce): The expiration logic of the order.
        extended_hours (Optional[float]): Whether the order can be executed during regular market hours.
        client_order_id (Optional[str]): A string to identify which client submitted the order.
        order_class (Optional[OrderClass]): The class of the order. Simple orders have no other legs.
        take_profit (Optional[TakeProfitRequest]): For orders with multiple legs, an order to exit a profitable trade.
        stop_loss (Optional[StopLossRequest]): For orders with multiple legs, an order to exit a losing trade.

    """

    def __init__(self, **data: Any) -> None:
        data["type"] = OrderType.MARKET

        super().__init__(**data)


class StopOrderRequest(OrderRequest):
    """
    Used to submit a stop order.

    Attributes
    ----------
        symbol (str): The symbol identifier for the asset being traded
        qty (Optional[float]): The number of shares to trade. Fractional qty for stocks only with market orders.
        notional (Optional[float]): The base currency value of the shares to trade. For stocks, only works with MarketOrders.
            **Does not work with qty**.
        side (OrderSide): Whether the order will buy or sell the asset.
        type (OrderType): The execution logic type of the order (market, limit, etc).
        time_in_force (TimeInForce): The expiration logic of the order.
        extended_hours (Optional[float]): Whether the order can be executed during regular market hours.
        client_order_id (Optional[str]): A string to identify which client submitted the order.
        order_class (Optional[OrderClass]): The class of the order. Simple orders have no other legs.
        take_profit (Optional[TakeProfitRequest]): For orders with multiple legs, an order to exit a profitable trade.
        stop_loss (Optional[StopLossRequest]): For orders with multiple legs, an order to exit a losing trade.
        stop_price (float): The price at which the stop order is converted to a market order or a stop limit
            order is converted to a limit order.
    """

    stop_price: float

    def __init__(self, **data: Any) -> None:
        data["type"] = OrderType.STOP

        super().__init__(**data)


class LimitOrderRequest(OrderRequest):
    """
    Used to submit a limit order.

    Attributes
    ----------
        symbol (str): The symbol identifier for the asset being traded
        qty (Optional[float]): The number of shares to trade. Fractional qty for stocks only with market orders.
        notional (Optional[float]): The base currency value of the shares to trade. For stocks, only works with MarketOrders.
            **Does not work with qty**.
        side (OrderSide): Whether the order will buy or sell the asset.
        type (OrderType): The execution logic type of the order (market, limit, etc).
        time_in_force (TimeInForce): The expiration logic of the order.
        extended_hours (Optional[float]): Whether the order can be executed during regular market hours.
        client_order_id (Optional[str]): A string to identify which client submitted the order.
        order_class (Optional[OrderClass]): The class of the order. Simple orders have no other legs.
        take_profit (Optional[TakeProfitRequest]): For orders with multiple legs, an order to exit a profitable trade.
        stop_loss (Optional[StopLossRequest]): For orders with multiple legs, an order to exit a losing trade.
        limit_price (float): The worst fill price for a limit or stop limit order.
    """

    limit_price: float

    def __init__(self, **data: Any) -> None:
        data["type"] = OrderType.LIMIT

        super().__init__(**data)


class StopLimitOrderRequest(OrderRequest):
    """
    Used to submit a stop limit order.

    Attributes
    ----------
        symbol (str): The symbol identifier for the asset being traded
        qty (Optional[float]): The number of shares to trade. Fractional qty for stocks only with market orders.
        notional (Optional[float]): The base currency value of the shares to trade. For stocks, only works with MarketOrders.
            **Does not work with qty**.
        side (OrderSide): Whether the order will buy or sell the asset.
        type (OrderType): The execution logic type of the order (market, limit, etc).
        time_in_force (TimeInForce): The expiration logic of the order.
        extended_hours (Optional[float]): Whether the order can be executed during regular market hours.
        client_order_id (Optional[str]): A string to identify which client submitted the order.
        order_class (Optional[OrderClass]): The class of the order. Simple orders have no other legs.
        take_profit (Optional[TakeProfitRequest]): For orders with multiple legs, an order to exit a profitable trade.
        stop_loss (Optional[StopLossRequest]): For orders with multiple legs, an order to exit a losing trade.
        stop_price (float): The price at which the stop order is converted to a market order or a stop limit
            order is converted to a limit order.
        limit_price (float): The worst fill price for a limit or stop limit order.
    """

    stop_price: float
    limit_price: float

    def __init__(self, **data: Any) -> None:
        data["type"] = OrderType.STOP_LIMIT

        super().__init__(**data)


class TrailingStopOrderRequest(OrderRequest):
    """
    Used to submit a trailing stop order.

    Attributes
    ----------
        symbol (str): The symbol identifier for the asset being traded
        qty (Optional[float]): The number of shares to trade. Fractional qty for stocks only with market orders.
        notional (Optional[float]): The base currency value of the shares to trade. For stocks, only works with MarketOrders.
            **Does not work with qty**.
        side (OrderSide): Whether the order will buy or sell the asset.
        type (OrderType): The execution logic type of the order (market, limit, etc).
        time_in_force (TimeInForce): The expiration logic of the order.
        extended_hours (Optional[float]): Whether the order can be executed during regular market hours.
        client_order_id (Optional[str]): A string to identify which client submitted the order.
        order_class (Optional[OrderClass]): The class of the order. Simple orders have no other legs.
        take_profit (Optional[TakeProfitRequest]): For orders with multiple legs, an order to exit a profitable trade.
        stop_loss (Optional[StopLossRequest]): For orders with multiple legs, an order to exit a losing trade.
        trail_price (Optional[float]): The absolute price difference by which the trailing stop will trail.
        trail_percent (Optional[float]): The percent price difference by which the trailing stop will trail.
    """

    trail_price: float | None = None
    trail_percent: float | None = None

    def __init__(self, **data: Any) -> None:
        data["type"] = OrderType.TRAILING_STOP

        super().__init__(**data)

    @model_validator(mode="before")
    @classmethod
    def root_validator(cls, values: dict) -> dict:
        """Validate that trail_price or trail_percent is set, but not both."""
        trail_percent_set = "trail_percent" in values and values["trail_percent"] is not None
        trail_price_set = "trail_price" in values and values["trail_price"] is not None

        if not trail_percent_set and not trail_price_set:
            raise ValueError(
                "Either trail_percent or trail_price must be set for a trailing stop order."
            )
        if trail_percent_set and trail_price_set:
            raise ValueError("Both trail_percent and trail_price cannot be set.")

        return values


class GetCorporateAnnouncementsRequest(NonEmptyRequest):
    """
    Contains parameters for querying corporate action data.

    Attributes
    ----------
        ca_types (List[CorporateActionType]): A list of corporate action types.
        since (date): The start (inclusive) of the date range when searching corporate action announcements.
            The date range is limited to 90 days.
        until (date): The end (inclusive) of the date range when searching corporate action announcements.
            The date range is limited to 90 days.
        symbol (Optional[str]): The symbol of the company initiating the announcement.
        cusip (Optional[str]): The CUSIP of the company initiating the announcement.
        date_type (Optional[CorporateActionDateType]): The date type for the announcement.
    """

    ca_types: list[CorporateActionType]
    since: date
    until: date
    symbol: str | None = None
    cusip: str | None = None
    date_type: CorporateActionDateType | None = None

    @model_validator(mode="before")
    @classmethod
    def root_validator(cls, values: dict) -> dict:
        """Validate that the date range is not greater than 90 days."""
        since = pd.Timestamp(values.get("since")).date()
        until = pd.Timestamp(values.get("until")).date()

        if since is not None and until is not None and (until - since) > timedelta(days=90):
            raise ValueError("The date range is limited to 90 days.")

        return values
