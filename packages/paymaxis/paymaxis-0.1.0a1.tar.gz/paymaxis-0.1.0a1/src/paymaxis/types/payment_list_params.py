# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["PaymentListParams", "Created", "Updated"]


class PaymentListParams(TypedDict, total=False):
    created: Created

    limit: int
    """The numbers of items to return. Default is 50."""

    offset: int
    """The number of items to skip before starting to collect the result set.

    Default is 0.
    """

    updated: Updated


class Created(TypedDict, total=False):
    gte: str
    """If passed, return only payments created at or after the specified time"""

    lt: str
    """If passed, return only payments created strictly before the specified time"""


class Updated(TypedDict, total=False):
    gte: str
    """If passed, return only payments updated at or after the specified time"""

    lt: str
    """If passed, return only payments updated strictly before the specified time"""
