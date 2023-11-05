"""Funding models."""
from datetime import datetime
from uuid import UUID

from pydantic import Field

from pypaca.broker.enums import (
    ACHRelationshipStatus,
    BankAccountType,
    BankStatus,
    FeePaymentMethod,
    IdentifierType,
    TransferDirection,
    TransferStatus,
    TransferType,
)
from pypaca.rest.models import ModelWithID


class ACHRelationship(ModelWithID):
    """
    ACHRelationship model.

    Attributes
    ----------
        id (UUID): ID of Relationship
        account_id (UUID): ID of the Account this ACHRelationship is tied to
        created_at (datetime): Date and time this relationship was created
        updated_at (datetime): Date and time of when this relationship was last updated
        status (ACHRelationshipStatus): Current status of the relationship
        account_owner_name (str): Full name of the account owner
        bank_account_type (BankAccountType): The kind of bank account this relationship points to
        bank_account_number (str): The number of bank account that the relationship points to
        bank_routing_number (str): Routing number for the bank account
        nickname (str): User provided name for account
        processor_token (Optional[str]): If you are using Plaid, then this is a Plaid processor token.
    """

    account_id: UUID
    created_at: datetime
    updated_at: datetime
    status: ACHRelationshipStatus
    account_owner_name: str
    bank_account_type: BankAccountType
    bank_account_number: str
    bank_routing_number: str
    nickname: str | None = None
    processor_token: str | None = None


class Bank(ModelWithID):
    """
    Bank model.

    Attributes
    ----------
        id (UUID): ID of Bank.
        account_id (UUID): ID of the Account this Bank is tied to.
        created_at (datetime): Date and time this Bank was created.
        updated_at (datetime): Date and time of when this Bank was last updated.
        name (str): Name of the bank.
        status (BankStatus): The status of the bank connection.
        country (str): Country where bank account is located.
        state_province (str): State/Province where bank is located.
        postal_code (str): Postal code where bank is located.
        city (str): City where bank is located.
        street_address (str): Street address where bank is located.
        account_number (str): The bank account number.
        bank_code (str): The bank account code.
        bank_code_type (IdentifierType): The bank identifier.
    """

    account_id: UUID
    created_at: datetime
    updated_at: datetime
    name: str
    status: BankStatus
    country: str
    state_province: str
    postal_code: str
    city: str
    street_address: str
    account_number: str
    bank_code: str
    bank_code_type: IdentifierType


class Transfer(ModelWithID):
    """
    Transfer model.

    Attributes
    ----------
        id (UUID): ID of Transfer.
        account_id (UUID): ID of the Account this Transfer is tied to.
        created_at (datetime): Date and time when this Transfer was created.
        updated_at (datetime): Date and time of when this Transfer was last updated.
        expires_at (datetime): Date and time of when this Transfer will expire.
        relationship_id (UUID): ID of the funding relationship used to make the transfer.
        amount (str): The amount the recipient will receive after any applicable fees are deducted.
        type (TransferType): The type of transfer.
        status (TransferStatus): The status of the transfer.
        direction (TransferDirection): The direction of the transfer.
        reason (Optional[str]): Reasoning associated with the current status.
        requested_amount (Optional[str]): Amount entered upon creation of a transfer entity.
        fee (Optional[str]): Dollar amount of any applicable fees.
        fee_payment_method (Optional[FeePaymentMethod]): Denotes how any applicable fees will be paid.
        additional_information (Optional[str]): Additional information provided with wire transfers.
    """

    account_id: UUID
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    relationship_id: UUID
    amount: str
    type_: TransferType = Field(alias="type")
    status: TransferStatus
    direction: TransferDirection
    reason: str | None = None
    requested_amount: str | None = None
    fee: str | None = None
    fee_payment_method: FeePaymentMethod | None = None
    additional_information: str | None = None
