# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import datetime
from typing import Union
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["RecentDarkpoolTradeListParams"]


class RecentDarkpoolTradeListParams(TypedDict, total=False):
    date: Annotated[Union[str, datetime.date], PropertyInfo(format="iso8601")]
    """Date to filter darkpool transactions."""

    limit: int
    """How many items to return. Default is 100. Max is 200. Minimum is 1."""
