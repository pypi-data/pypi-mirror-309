# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["SubscriptionDeleteParams"]


class SubscriptionDeleteParams(TypedDict, total=False):
    ids: List[str]
    """List of event subscription ids to delete"""
