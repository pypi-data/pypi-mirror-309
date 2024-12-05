# coding: utf-8

"""
    Carbon

    Connect external data to LLMs, no matter the source.

    The version of the OpenAPI document: 1.0.0
    Generated by: https://konfigthis.com
"""

from datetime import datetime, date
import typing
from enum import Enum
from typing_extensions import TypedDict, Literal, TYPE_CHECKING
from pydantic import BaseModel, Field, RootModel, ConfigDict

from carbon.pydantic.user import User

class PRComment(BaseModel):
    id: int = Field(alias='id')

    pull_request_review_id: typing.Optional[int] = Field(alias='pull_request_review_id')

    url: str = Field(alias='url')

    diff_hunk: str = Field(alias='diff_hunk')

    path: str = Field(alias='path')

    user: User = Field(alias='user')

    body: str = Field(alias='body')

    created_at: str = Field(alias='created_at')

    updated_at: str = Field(alias='updated_at')

    start_line: typing.Optional[int] = Field(alias='start_line')

    line: typing.Optional[int] = Field(alias='line')

    remote_data: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = Field(alias='remote_data')

    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True
    )
