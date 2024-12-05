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

from carbon.type.address import Address
from carbon.type.event import Event
from carbon.type.partial_owner_nullable import PartialOwnerNullable
from carbon.type.phone_number import PhoneNumber
from carbon.type.task import Task

class RequiredAccount(TypedDict):
    description: typing.Optional[str]

    id: str

    owner: typing.Optional[PartialOwnerNullable]

    name: typing.Optional[str]

    industry: typing.Optional[str]

    website: typing.Optional[str]

    number_of_employees: typing.Optional[int]

    addresses: typing.List[Address]

    phone_numbers: typing.List[PhoneNumber]

    last_activity_at: typing.Optional[str]

    created_at: str

    updated_at: str

    is_deleted: bool

    remote_data: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]


class OptionalAccount(TypedDict, total=False):
    tasks: typing.Optional[typing.List[Task]]

    events: typing.Optional[typing.List[Event]]

class Account(RequiredAccount, OptionalAccount):
    pass
