"""Credentials module."""
from pydantic import model_validator
from pydantic_settings import BaseSettings


class Credentials(BaseSettings):
    """Credentials for the REST API."""

    api_key: str | None = None
    secret_key: str | None = None
    oauth_token: str | None = None

    @model_validator(mode="after")
    def validate_credentials(self) -> "Credentials":
        """Validate the credentials."""
        if not self.oauth_token and not self.api_key:
            raise ValueError("You must supply a method of authentication")

        if self.oauth_token and (self.api_key or self.secret_key):
            raise ValueError("Either an oauth_token or an api_key may be supplied, but not both")

        if not self.oauth_token and not (self.api_key and self.secret_key):
            raise ValueError("A corresponding secret_key must be supplied with the api_key")
        return self
