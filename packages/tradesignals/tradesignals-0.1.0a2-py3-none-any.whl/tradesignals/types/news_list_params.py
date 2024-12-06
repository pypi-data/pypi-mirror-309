# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import datetime
from typing import Union
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["NewsListParams"]


class NewsListParams(TypedDict, total=False):
    date: Annotated[Union[str, datetime.date], PropertyInfo(format="iso8601")]
    """Date to filter news articles."""

    symbols: str
    """Comma-separated list of stock symbols to filter news."""
