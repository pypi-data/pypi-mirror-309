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


class ChunkPropertiesNullable(BaseModel):
    set_page_as_boundary: typing.Optional[bool] = Field(None, alias='set_page_as_boundary')

    prepend_filename_to_chunks: typing.Optional[bool] = Field(None, alias='prepend_filename_to_chunks')

    max_items_per_chunk: typing.Optional[typing.Optional[int]] = Field(None, alias='max_items_per_chunk')

    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True
    )
