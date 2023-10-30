"""Rest client."""
import base64
import time
from collections.abc import Iterator
from itertools import chain

from pydantic import BaseModel
from requests import Session
from requests.exceptions import HTTPError

from pypaca import __version__
from pypaca.rest.enums import BaseURL, PaginationType
from pypaca.rest.exceptions import APIError, RetryError
from pypaca.rest.types import Credentials, HTTPResult, PageItem, RawData


class RestClient:
    """Abstract base class for REST clients."""

    def __init__(  # noqa: PLR0913
        self,
        base_url: BaseURL | str,
        api_key: str | None = None,
        secret_key: str | None = None,
        oauth_token: str | None = None,
        use_basic_auth: bool = False,
        api_version: str = "v2",
        sandbox: bool = False,
        retry_attempts: int = 3,
        retry_wait_seconds: int = 3,
        retry_exception_codes: tuple[int] = (429, 504),
    ) -> None:
        """Abstract base class for REST clients. Handles submitting HTTP requests to Alpaca API endpoints.

        Args:
            base_url (Union[BaseURL, str]): The base url to target requests to. Should be an instance of BaseURL, but
              allows for raw str if you need to override
            api_key (Optional[str]): The api key string for authentication.
            secret_key (Optional[str]): The corresponding secret key string for the api key.
            oauth_token (Optional[str]): The oauth token if authenticating via OAuth.
            use_basic_auth (bool): Whether API requests should use basic authorization headers.
            api_version (Optional[str]): The API version for the endpoints.
            sandbox (bool): False if the live API should be used.
            raw_data (bool): Whether API responses should be wrapped in data models or returned raw.
            retry_attempts (Optional[int]): The number of times to retry a request that returns a RetryError.
            retry_wait_seconds (Optional[int]): The number of seconds to wait between requests before retrying.
            retry_exception_codes (Optional[List[int]]): The API exception codes to retry a request on.
        """
        self._api_key, self._secret_key, self._oauth_token = self._validate_credentials(
            api_key, secret_key, oauth_token
        )
        self._api_version: str = api_version
        self._base_url: BaseURL | str = base_url
        self._sandbox: bool = sandbox
        self._use_basic_auth: bool = use_basic_auth
        self._session: Session = Session()

        # setting up request retry configurations
        self._retry = retry_attempts
        self._retry_wait = retry_wait_seconds
        self._retry_codes = retry_exception_codes

        if retry_attempts and retry_attempts > 0:
            self._retry = retry_attempts

        if retry_wait_seconds and retry_wait_seconds > 0:
            self._retry_wait = retry_wait_seconds

        if retry_exception_codes:
            self._retry_codes = retry_exception_codes

    def _request(  # noqa: PLR0913
        self,
        method: str,
        path: str,
        data: dict | str | None = None,
        base_url: BaseURL | str | None = None,
        api_version: str | None = None,
    ) -> HTTPResult:
        """Prepare and submit HTTP requests to given API endpoint and returns response.

        Parameters
        ----------
        method : str
            The API endpoint HTTP method
        path : str
            The API endpoint path
        data : Union[dict, str], optional
            Either the payload in json format, query params urlencoded, or a dict of values to be converted to
            appropriate format based on `method`. Defaults to None.
        base_url : Union[BaseURL, str], optional
            The base URL of the API. Defaults to None.
        api_version : str, optional
            The API version. Defaults to None.

        Returns
        -------
        HTTPResult
            The response from the API

        Raises
        ------
        RetryError
            If the request fails due to a 429 (Rate Limit) error.
        """
        base_url = base_url or self._base_url
        version = api_version if api_version else self._api_version
        url: str = base_url + "/" + version + path

        headers = self._get_default_headers()

        opts = {
            "headers": headers,
            # Since we allow users to set endpoint URL via env var,
            # human error to put non-SSL endpoint could exploit
            # uncanny issues in non-GET request redirecting http->https.
            # It's better to fail early if the URL isn't right.
            "allow_redirects": False,
        }

        if method.upper() in ["GET", "DELETE"]:
            opts["params"] = data
        else:
            opts["json"] = data

        retry = self._retry

        while retry >= 0:
            try:
                return self._one_request(method, url, opts, retry)
            except RetryError:
                time.sleep(self._retry_wait)
                retry -= 1
                continue
        return None

    def _get_default_headers(self) -> dict:
        """
        Return a dict with some default headers set; ie AUTH headers and such that should be useful on all requests.

        Extracted for cases when using the default request functions are insufficient.

        Returns
        -------
            dict: The resulting dict of headers
        """
        headers = self._get_auth_headers()

        headers["User-Agent"] = "APCA-PY/" + __version__

        return headers

    def _get_auth_headers(self) -> dict:
        """
        Get the auth headers for a request.

        Meant to be overridden in clients that don't use this format for requests,

        Returns
        -------
            dict: A dict containing the expected auth headers
        """
        headers = {}

        if self._oauth_token:
            headers["Authorization"] = "Bearer " + self._oauth_token
        elif self._use_basic_auth:
            api_key_secret = f"{self._api_key}:{self._secret_key}".encode()
            encoded_api_key_secret = base64.b64encode(api_key_secret).decode("utf-8")
            headers["Authorization"] = "Basic " + encoded_api_key_secret
        else:
            headers["APCA-API-KEY-ID"] = self._api_key
            headers["APCA-API-SECRET-KEY"] = self._secret_key

        return headers

    def _one_request(self, method: str, url: str, opts: dict, retry: int) -> dict:
        """
        Perform one request, possibly raising RetryError in the case the response is 429.

        Otherwise, if error text contain "code" string,
        then it decodes to json object and returns APIError.
        Returns the body json in the 200 status.

        Parameters
        ----------
            method (str): The HTTP method - GET, POST, etc
            url (str): The API endpoint URL
            opts (dict): Contains optional parameters including headers and parameters
            retry (int): The number of times to retry in case of RetryError

        Raises
        ------
            RetryError: Raised if request produces 429 error and retry limit has not been reached
            APIError: Raised if API returns an error

        Returns
        -------
            dict: The response data
        """
        response = self._session.request(method, url, **opts)

        try:
            response.raise_for_status()
        except HTTPError as http_error:
            # retry if we hit Rate Limit
            if response.status_code in self._retry_codes and retry > 0:
                raise RetryError from http_error

            raise APIError(http_error) from http_error

        if response.text != "":
            return response.json()
        return None

    def get(self, path: str, data: dict | str | None = None, **kwargs) -> HTTPResult:
        """
        Perform a single GET request.

        Parameters
        ----------
            path (str): The API endpoint path
            data (Union[dict, str], optional): Query parameters to send, either
            as a str urlencoded, or a dict of values to be converted. Defaults to None.

        Returns
        -------
            dict: The response
        """
        return self._request("GET", path, data, **kwargs)

    def post(self, path: str, data: dict | (list[dict] | str) | None = None) -> HTTPResult:
        """
        Perform a single POST request.

        Parameters
        ----------
            path (str): The API endpoint path
            data (Union[dict, str], optional): The json payload if str, or a dict of values to be converted.
             Defaults to None.

        Returns
        -------
            dict: The response
        """
        return self._request("POST", path, data)

    def put(self, path: str, data: dict | str | None = None) -> dict:
        """
        Perform a single PUT request.

        Parameters
        ----------
            path (str): The API endpoint path
            data (Union[dict, str], optional): The json payload if str, or a dict of values to be converted.
             Defaults to None.

        Returns
        -------
            dict: The response
        """
        return self._request("PUT", path, data)

    def patch(self, path: str, data: dict | str | None = None) -> dict:
        """
        Perform a single PATCH request.

        Parameters
        ----------
            path (str): The API endpoint path
            data (Union[dict, str], optional): The json payload if str, or a dict of values to be converted.
             Defaults to None.

        Returns
        -------
            dict: The response
        """
        return self._request("PATCH", path, data)

    def delete(self, path, data: dict | str | None = None) -> dict:
        """
        Perform a single DELETE request.

        Parameters
        ----------
            path (str): The API endpoint path
            data (Union[dict, str], optional): The payload if any. Defaults to None.

        Returns
        -------
            dict: The response
        """
        return self._request("DELETE", path, data)

    # TODO: Refactor to be able to handle both parsing to types and parsing to collections of types (parse_as_obj)
    def response_wrapper(
        self, model: type[BaseModel], raw_data: RawData, **kwargs
    ) -> BaseModel | RawData:
        """
        Wrap the response from the API.

        To allow the user to get raw response from the api, we wrap all
        functions with this method, checking if the user has set raw_data
        bool. if they didn't, we wrap the response with a BaseModel object.

        Parameters
        ----------
            model (Type[BaseModel]): Class that response will be wrapped in
            raw_data (RawData): The raw data from API in dictionary
            kwargs : Any constructor parameters necessary for the base model

        Returns
        -------
            Union[BaseModel, RawData]: either raw or parsed data
        """
        return model(raw_data=raw_data, **kwargs)

    @staticmethod
    def _validate_pagination(
        max_items_limit: int | None, handle_pagination: PaginationType | None
    ) -> PaginationType:
        """Private method for validating the max_items_limit and handle_pagination arguments."""
        if handle_pagination is None:
            handle_pagination = PaginationType.FULL

        if handle_pagination != PaginationType.FULL and max_items_limit is not None:
            raise ValueError("max_items_limit can only be specified for PaginationType.FULL")
        return handle_pagination

    @staticmethod
    def _return_paginated_result(
        iterator: Iterator[PageItem], handle_pagination: PaginationType
    ) -> list[PageItem] | Iterator[list[PageItem]]:
        """Private method for converting an iterator that yields results to the proper pagination type result."""
        if handle_pagination == PaginationType.NONE:
            # user wants no pagination, so just do a single page
            return next(iterator)
        if handle_pagination == PaginationType.FULL:
            # the iterator returns "pages", so we use chain to flatten them all into 1 list
            return list(chain.from_iterable(iterator))
        if handle_pagination == PaginationType.ITERATOR:
            return iterator
        raise ValueError(f"Invalid pagination type: {handle_pagination}.")

    @staticmethod
    def _validate_credentials(
        api_key: str | None = None,
        secret_key: str | None = None,
        oauth_token: str | None = None,
    ) -> Credentials:
        """
        Gather API credentials from parameters and environment variables, and validates them.

        Parameters
        ----------
            api_key (Optional[str]): The API key for authentication. Defaults to None.
            secret_key (Optional[str]): The secret key for authentication. Defaults to None.
            oauth_token (Optional[str]): The oauth token if authenticating via OAuth. Defaults to None.

        Raises
        ------
             ValueError: If the combination of keys and tokens provided are not valid.

        Returns
        -------
            Credentials: The set of validated authentication keys
        """
        if not oauth_token and not api_key:
            raise ValueError("You must supply a method of authentication")

        if oauth_token and (api_key or secret_key):
            raise ValueError("Either an oauth_token or an api_key may be supplied, but not both")

        if not oauth_token and not (api_key and secret_key):
            raise ValueError("A corresponding secret_key must be supplied with the api_key")

        return api_key, secret_key, oauth_token
