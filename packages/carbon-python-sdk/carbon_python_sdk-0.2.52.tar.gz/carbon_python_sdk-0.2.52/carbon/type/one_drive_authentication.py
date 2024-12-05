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


class RequiredOneDriveAuthentication(TypedDict):
    source: str

    access_token: str


class OptionalOneDriveAuthentication(TypedDict, total=False):
    refresh_token: typing.Optional[str]

    tenant_name: typing.Optional[str]

class OneDriveAuthentication(RequiredOneDriveAuthentication, OptionalOneDriveAuthentication):
    pass
