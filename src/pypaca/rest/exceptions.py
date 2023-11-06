"""Exceptions module."""
import json
import pprint

from pydantic import BaseModel, TypeAdapter, ValidationError
from requests import Request, Response
from requests.exceptions import HTTPError

from pypaca.rest.types import RawData


class ErrorBody(BaseModel):
    """Represent the body of an API error response."""

    code: int
    message: str


class PDTErrorBody(ErrorBody):
    """Represent the body of the API error in case of patter day trading."""

    day_trading_buying_power: float
    max_dtbp_used: float
    max_dtbp_used_so_far: float
    open_orders: int
    symbol: str


class BuyingPowerErrorBody(ErrorBody):
    """Represent the body of the API error in case of insufficient buying power."""

    buying_power: float
    cost_basis: float


class APIError(Exception):
    """
    Represent API related error.

    Parameters
    ----------
    error : str
        The error message.
    http_error : HTTPError, optional
        The HTTP error, by default None.

    Attributes
    ----------
    request : Request
        The HTTP request.
    response : Response
        The HTTP response.
    status_code : int
        The HTTP status code.
    body : Union[ErrorBody, Dict[str, Any]]
        The body of the response. It will be a base model or the raw data if the pydantic validation fails.
    code : int
        The Alpaca error code from the response body.
    """

    def __init__(
        self,
        http_error: HTTPError,
    ) -> None:
        """
        Initialize the APIError instance.

        Parameters
        ----------
        http_error : HTTPError
            The HTTP error.

        Returns
        -------
        None
        """
        self._http_error = http_error
        super().__init__(self.__repr__())

    def __repr__(self) -> str:
        """
        Return a string representation of the APIError instance.

        This method overrides the default `__repr__` method and includes the status code,
        body, and HTTP error of the APIError instance in the string representation.

        Returns
        -------
        str
            A string representation of the APIError instance.
        """
        return pprint.pformat(
            {
                "status_code": self.status_code,
                "body": self.body,
                "http_error": self._http_error,
            },
            sort_dicts=False,
            compact=True,
        )

    @property
    def request(self) -> Request:
        """Return the HTTP request."""
        assert isinstance(self._http_error.request, Request)
        return self._http_error.request

    @property
    def response(self) -> Response:
        """Return the HTTP response."""
        assert isinstance(self._http_error.response, Response)
        return self._http_error.response

    @property
    def status_code(self) -> int:
        """Return the HTTP status code."""
        return self.response.status_code

    @property
    def body(self) -> ErrorBody | RawData:
        """Return the body of the response."""
        _body: dict = json.loads(self.response.content)
        _models: list[type[ErrorBody]] = [
            ErrorBody,
            BuyingPowerErrorBody,
            PDTErrorBody,
        ]
        for base_model in _models:
            if set(base_model.model_fields.keys()) == set(_body.keys()):
                try:
                    return TypeAdapter(base_model).validate_python(_body)
                except ValidationError:
                    return _body
        return _body

    @property
    def code(self) -> int:
        """Return the Alpaca error code from the response body."""
        if isinstance(self.body, ErrorBody):
            return self.body.code
        if isinstance(self.body, dict):
            return int(self.body.get("code", None))
        return int(json.loads(self.response.content)["code"])


class RetryError(Exception):
    """Thrown by RESTClient's internally to represent a request that should be retried."""
