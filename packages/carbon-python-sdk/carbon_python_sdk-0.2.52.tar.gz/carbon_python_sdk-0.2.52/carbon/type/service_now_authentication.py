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


class RequiredServiceNowAuthentication(TypedDict):
    source: str

    access_token: str

    instance_subdomain: str

    client_id: str

    client_secret: str

    redirect_uri: str


class OptionalServiceNowAuthentication(TypedDict, total=False):
    refresh_token: typing.Optional[str]

class ServiceNowAuthentication(RequiredServiceNowAuthentication, OptionalServiceNowAuthentication):
    pass
