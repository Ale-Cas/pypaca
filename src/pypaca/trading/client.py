"""Trading API client."""

from pydantic import TypeAdapter

from pypaca.rest import BaseURL
from pypaca.rest.rest import RestClient
from pypaca.trading.enums import Routes
from pypaca.trading.models import AccountConfiguration, TradeAccount
from pypaca.trading.requests import PatchAccountConfiguration


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
            TradeAccount: The account details
        """
        return TypeAdapter(TradeAccount).validate_python(self.get(Routes.ACCOUNT.value))

    def get_account_configurations(self) -> AccountConfiguration:
        """
        Return account configuration details.

        Contains information like shorting, margin multiplier
        trader confirmation emails, and Pattern Day Trading (PDT) checks.

        Returns
        -------
            AccountConfiguration: The account configuration details
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

        Returns
        -------
            TradeAccountConfiguration: The account configuration details
        """
        return TypeAdapter(AccountConfiguration).validate_python(
            self.patch(
                Routes.ACCOUNT_CONFIGURATIONS.value, data=account_configurations.model_dump()
            )
        )
