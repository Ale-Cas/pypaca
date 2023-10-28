"""Enums module for the package."""

from enum import Enum


class BaseURL(str, Enum):
    """
    Base urls for API endpoints.

    Parameters
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
