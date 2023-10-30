"""Custom types for the rest module."""
from typing import Any, TypeVar

RawData = dict[str, Any]

# TODO: Refine this type
HTTPResult = dict | list[dict] | Any
Credentials = tuple[str, str]

PageItem = TypeVar("PageItem")  # Generic type for an item from a paginated request.
