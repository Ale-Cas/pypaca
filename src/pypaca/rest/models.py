"""Common models."""


from uuid import UUID

from pydantic import BaseModel, Field


class ModelWithID(BaseModel):
    """Base model for responses with IDs that are UUIDs."""

    id_: UUID = Field(..., alias="id")
