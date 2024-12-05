# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["CategoryUpdateParams"]


class CategoryUpdateParams(TypedDict, total=False):
    description: Required[str]

    name: Required[str]
