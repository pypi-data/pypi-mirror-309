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
from carbon.type.email import Email
from carbon.type.event import Event
from carbon.type.partial_account_nullable import PartialAccountNullable
from carbon.type.partial_contact_nullable import PartialContactNullable
from carbon.type.partial_owner import PartialOwner
from carbon.type.phone_number import PhoneNumber
from carbon.type.task import Task

class RequiredLead(TypedDict):
    title: typing.Optional[str]

    description: typing.Optional[str]

    id: str

    owner: PartialOwner

    source: typing.Optional[str]

    status: typing.Optional[str]

    company: typing.Optional[str]

    first_name: typing.Optional[str]

    last_name: typing.Optional[str]

    addresses: typing.List[Address]

    phone_numbers: typing.List[PhoneNumber]

    emails: typing.List[Email]

    converted_at: typing.Optional[str]

    converted_account: typing.Optional[PartialAccountNullable]

    converted_contact: typing.Optional[PartialContactNullable]

    last_activity_at: typing.Optional[str]

    created_at: str

    updated_at: str

    is_deleted: bool

    remote_data: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]


class OptionalLead(TypedDict, total=False):
    tasks: typing.Optional[typing.List[Task]]

    events: typing.Optional[typing.List[Event]]

class Lead(RequiredLead, OptionalLead):
    pass
