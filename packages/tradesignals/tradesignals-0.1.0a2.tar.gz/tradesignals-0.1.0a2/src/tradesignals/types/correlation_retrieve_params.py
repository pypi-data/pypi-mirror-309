# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import date
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["CorrelationRetrieveParams"]


class CorrelationRetrieveParams(TypedDict, total=False):
    symbols: Required[str]
    """Comma-separated list of stock symbols."""

    end_date: Annotated[Union[str, date], PropertyInfo(alias="endDate", format="iso8601")]
    """End date for the correlation data."""

    interval: Literal["1d", "1wk", "1mo"]
    """Data interval (e.g., '1d', '1wk')."""

    start_date: Annotated[Union[str, date], PropertyInfo(alias="startDate", format="iso8601")]
    """Start date for the correlation data."""
