# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["EventSubscription", "Data"]


class Data(BaseModel):
    ids: List[str]


class EventSubscription(BaseModel):
    data: Data

    message: str
