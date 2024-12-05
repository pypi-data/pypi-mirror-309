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

from carbon.type.partial_account_nullable import PartialAccountNullable
from carbon.type.partial_contact_nullable import PartialContactNullable
from carbon.type.partial_owner import PartialOwner

class RequiredEvent(TypedDict):
    description: typing.Optional[str]

    id: str

    owner: PartialOwner

    subject: typing.Optional[str]

    location: typing.Optional[str]

    is_all_day: bool

    start_date: typing.Optional[str]

    end_date: typing.Optional[str]

    account: typing.Optional[PartialAccountNullable]

    contact: typing.Optional[PartialContactNullable]

    created_at: str

    updated_at: str

    is_deleted: bool

    remote_data: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]

class OptionalEvent(TypedDict, total=False):
    pass

class Event(RequiredEvent, OptionalEvent):
    pass
