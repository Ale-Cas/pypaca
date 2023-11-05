"""Custom types for the rest module."""
from typing import Any, TypeVar

HTTPResult = dict | list[dict] | Any
RawData = dict[str, Any] | list[dict] | str | None
PageItem = TypeVar("PageItem")  # Generic type for an item from a paginated request.
