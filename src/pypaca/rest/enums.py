"""Enums module for the package."""

from enum import Enum


class BaseURL(str, Enum):
    """
    Base urls for API endpoints.

    Attributes
    ----------
    BROKER_SANDBOX : str
        The base url for the Alpaca broker API sandbox.
    BROKER_PRODUCTION : str
        The base url for the Alpaca broker API production.
    TRADING_PAPER : str
        The base url for the Alpaca trading API paper trading.
    TRADING_LIVE : str
        The base url for the Alpaca trading API live trading.
    DATA : str
        The base url for the Alpaca data API.
    MARKET_DATA_STREAM : str
        The base url for the Alpaca market data streaming API.
    TRADING_STREAM_PAPER : str
        The base url for the Alpaca trading streaming API for paper trading.
    TRADING_STREAM_LIVE : str
        The base url for the Alpaca trading streaming API for live trading.
    """

    BROKER_SANDBOX = "https://broker-api.sandbox.alpaca.markets"
    BROKER_PRODUCTION = "https://broker-api.alpaca.markets"
    TRADING_PAPER = "https://paper-api.alpaca.markets"
    TRADING_LIVE = "https://api.alpaca.markets"
    DATA = "https://data.alpaca.markets"
    MARKET_DATA_STREAM = "wss://stream.data.alpaca.markets"
    TRADING_STREAM_PAPER = "wss://paper-api.alpaca.markets/stream"
    TRADING_STREAM_LIVE = "wss://api.alpaca.markets/stream"


class PaginationType(str, Enum):
    """
    An enum for choosing what type of pagination of results you'd like for BrokerClient functions that support pagination.

    Attributes
    ----------
        NONE: Requests that we perform no pagination of results and just return the single response the API gave us.
        FULL: Requests that we perform all the pagination and return just a single List/dict/etc containing all the
          results. This is the default for most functions.
        ITERATOR: Requests that we return an Iterator that yields one "page" of results at a time
    """

    NONE = "none"
    FULL = "full"
    ITERATOR = "iterator"


class Sort(str, Enum):
    """
    An enum for specifying the sort order of results.

    Attributes
    ----------
        ASC: Requests that we sort the results in ascending order.
        DESC: Requests that we sort the results in descending order.
    """

    ASC = "asc"
    DESC = "desc"


class SupportedCurrencies(str, Enum):
    """
    The various currencies that can be supported for LCT.

    see https://alpaca.markets/support/local-currency-trading-faq
    """

    USD = "USD"
    GBP = "GBP"
    CHF = "CHF"
    EUR = "EUR"
    CAD = "CAD"
    JPY = "JPY"
    TRY = "TRY"
    AUD = "AUD"
    CZK = "CZK"
    SEK = "SEK"
    DKK = "DKK"
    SGD = "SGD"
    HKD = "HKD"
    HUF = "HUF"
    NZD = "NZD"
    NOK = "NOK"
    PLN = "PLN"
