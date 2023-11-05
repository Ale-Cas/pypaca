"""Pagination utilities."""
from collections.abc import Iterator
from itertools import chain

from pydantic import BaseModel

from pypaca.rest.enums import PaginationType


def validate_pagination(
    max_items_limit: int | None, handle_pagination: PaginationType | None
) -> PaginationType:
    """Private method for validating the max_items_limit and handle_pagination arguments."""
    if handle_pagination is None:
        handle_pagination = PaginationType.FULL

    if handle_pagination != PaginationType.FULL and max_items_limit is not None:
        raise ValueError("max_items_limit can only be specified for PaginationType.FULL")
    return handle_pagination


def return_paginated_result(
    iterator: Iterator[list[BaseModel]], handle_pagination: PaginationType
) -> list[BaseModel] | Iterator[list[BaseModel]]:
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
