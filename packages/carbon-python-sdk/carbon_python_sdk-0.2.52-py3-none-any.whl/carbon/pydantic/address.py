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


class Address(BaseModel):
    street_1: typing.Optional[str] = Field(alias='street_1')

    street_2: typing.Optional[str] = Field(alias='street_2')

    city: typing.Optional[str] = Field(alias='city')

    state: typing.Optional[str] = Field(alias='state')

    postal_code: typing.Optional[str] = Field(alias='postal_code')

    country: typing.Optional[str] = Field(alias='country')

    address_type: typing.Optional[str] = Field(alias='address_type')

    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True
    )
