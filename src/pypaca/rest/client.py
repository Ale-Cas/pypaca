"""Abstract base class for REST clients."""
from abc import ABC, abstractmethod
from typing import Any

from pypaca.rest.enums import BaseURL


class RestClient(ABC):
    """
    Abstract base class for REST clients.

    Parameters
    ----------
    base_url : BaseURL
        The base URL for the REST API.
    api_key : str
        The API key to use for authentication.
    secret_key : str
        The secret key to use for authentication.
    oauth_token : str, optional
        The OAuth token to use for authentication.
    use_basic_auth : bool, optional
        Whether to use basic authentication.
    api_version : str, optional
        The version of the REST API to use.
    sandbox : bool, optional
        Whether to use the sandbox environment.
    """

    def __init__(  # noqa: PLR0913
        self,
        base_url: BaseURL,
        api_key: str,
        secret_key: str,
        oauth_token: str | None = None,
        use_basic_auth: bool = False,
        api_version: str = "v2",
        sandbox: bool = False,
    ) -> None:
        super().__init__()

    @abstractmethod
    def get(self, url: str) -> Any:
        """
        Send a GET request to the specified URL with optional headers.

        Parameters
        ----------
        url : str
            The URL to send the GET request to.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        Any
            The response from the server.
        """

    @abstractmethod
    def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """
        Send a POST request to the specified URL with optional data and headers.

        Parameters
        ----------
        url : str
            The URL to send the POST request to.
        data : dict, optional
            Optional data to include in the request.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        Any
            The response from the server.
        """

    @abstractmethod
    def patch(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """
        Send a PATCH request to the specified URL with optional data and headers.

        Parameters
        ----------
        url : str
            The URL to send the PATCH request to.
        data : dict, optional
            Optional data to include in the request.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        Any
            The response from the server.
        """

    @abstractmethod
    def delete(self, url: str, headers: dict[str, str] | None = None) -> Any:
        """
        Send a DELETE request to the specified URL with optional headers.

        Parameters
        ----------
        url : str
            The URL to send the DELETE request to.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        Any
            The response from the server.
        """

    @abstractmethod
    def put(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """
        Send a PUT request to the specified URL with optional data and headers.

        Parameters
        ----------
        url : str
            The URL to send the PUT request to.
        data : dict, optional
            Optional data to include in the request.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        Any
            The response from the server.
        """
