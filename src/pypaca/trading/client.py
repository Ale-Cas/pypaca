"""Trading API client."""
from uuid import UUID

from pydantic import TypeAdapter

from pypaca.rest import BaseURL
from pypaca.rest.rest import RestClient
from pypaca.trading.enums import Routes
from pypaca.trading.models import AccountConfiguration, Order, TradeAccount
from pypaca.trading.requests import (
    CancelOrderResponse,
    GetOrderByIdRequest,
    GetOrdersRequest,
    OrderRequest,
    PatchAccountConfiguration,
)


class TradingClient(RestClient):
    """Trading API client."""

    def __init__(  # noqa: PLR0913
        self,
        api_key: str | None = None,
        secret_key: str | None = None,
        oauth_token: str | None = None,
        use_basic_auth: bool = False,
        sandbox: bool = True,
        retry_attempts: int = 3,
        retry_wait_seconds: int = 3,
        retry_exception_codes: tuple[int, ...] = (429, 504),
    ) -> None:
        """Initialize the TradingClient instance."""
        super().__init__(
            base_url=BaseURL.TRADING_PAPER if sandbox else BaseURL.TRADING_LIVE,
            api_key=api_key,
            secret_key=secret_key,
            oauth_token=oauth_token,
            use_basic_auth=use_basic_auth,
            api_version="v2",
            sandbox=sandbox,
            retry_attempts=retry_attempts,
            retry_wait_seconds=retry_wait_seconds,
            retry_exception_codes=retry_exception_codes,
        )

    def get_account(self) -> TradeAccount:
        """
        Return account details.

        Contains information like buying power, number of day trades, and account status.

        Returns
        -------
            TradeAccount: The account details.
        """
        return TypeAdapter(TradeAccount).validate_python(self.get(Routes.ACCOUNT.value))

    def get_account_configurations(self) -> AccountConfiguration:
        """
        Return account configuration details.

        Contains information like shorting, margin multiplier
        trader confirmation emails, and Pattern Day Trading (PDT) checks.

        Returns
        -------
            AccountConfiguration: The account configuration details.
        """
        return TypeAdapter(AccountConfiguration).validate_python(
            self.get(Routes.ACCOUNT_CONFIGURATIONS.value)
        )

    def set_account_configurations(
        self, account_configurations: PatchAccountConfiguration
    ) -> AccountConfiguration:
        """
        Set account configuration details.

        Change configurations like shorting, margin multiplier
        trader confirmation emails, and Pattern Day Trading (PDT) checks.

        Parameters
        ----------
        `account_configurations`: PatchAccountConfiguration
            The account configuration details to update.

        Returns
        -------
            TradeAccountConfiguration: The account configuration details.
        """
        return TypeAdapter(AccountConfiguration).validate_python(
            self.patch(
                Routes.ACCOUNT_CONFIGURATIONS.value,
                data=account_configurations.model_dump(by_alias=True),
            )
        )

    def submit_order(self, order: OrderRequest) -> Order:
        """
        Submit an order to buy or sell an asset.

        Contains information like buying power, number of day trades, and account status.

        Parameters
        ----------
        `order`: OrderRequest
            The order to submit.

        Returns
        -------
            Order: The order response.
        """
        return TypeAdapter(Order).validate_python(
            self.post(Routes.ORDERS.value, data=order.model_dump(by_alias=True))
        )

    def get_orders(
        self,
        request_parameters: GetOrdersRequest | None = None,
    ) -> list[Order]:
        """
        Get a list of orders.

        Parameters
        ----------
        `request_parameters`: GetOrdersRequest, optional
            The request parameters to filter the orders by.

        Returns
        -------
            list[Order]: The list of orders.
        """
        return TypeAdapter(list[Order]).validate_python(
            self.get(
                Routes.ORDERS.value,
                request_parameters.model_dump(by_alias=True) if request_parameters else None,
            )
        )

    def get_order_by_id(
        self,
        order_id: UUID,
        request_parameters: GetOrderByIdRequest | None = None,
    ) -> Order:
        """
        Get a list of orders.

        Parameters
        ----------
        `request_parameters`: GetOrdersRequest, optional
            The request parameters to filter the orders by.

        Returns
        -------
            Order: The list of orders.
        """
        return TypeAdapter(Order).validate_python(
            self.get(
                Routes.ORDERS.value + f"/{order_id}",
                request_parameters.model_dump(by_alias=True) if request_parameters else None,
            )
        )

    def get_order_by_client_id(
        self,
        client_order_id: UUID | str,
    ) -> Order:
        """
        Get a list of orders.

        Parameters
        ----------
        `request_parameters`: GetOrdersRequest, optional
            The request parameters to filter the orders by.

        Returns
        -------
            Order: The list of orders.
        """
        return TypeAdapter(Order).validate_python(
            self.get(
                Routes.ORDERS.value + ":by_client_order_id",
                data={"client_order_id": client_order_id},
            )
        )

    def cancel_orders(self) -> list[CancelOrderResponse]:
        """
        Cancel all orders.

        Returns
        -------
            list[CancelOrderResponse]: The list of HTTP statuses for each order attempted to be cancelled.
        """
        return TypeAdapter(list[CancelOrderResponse]).validate_python(
            self.delete(Routes.ORDERS.value)
        )

    def cancel_order_by_id(self, order_id: UUID) -> None:
        """
        Cancel a specific order by its order id.

        Parameters
        ----------
        order_id: UUID
            The unique uuid identifier of the order being cancelled.
        """
        self.delete(f"{Routes.ORDERS.value}/{order_id}")
