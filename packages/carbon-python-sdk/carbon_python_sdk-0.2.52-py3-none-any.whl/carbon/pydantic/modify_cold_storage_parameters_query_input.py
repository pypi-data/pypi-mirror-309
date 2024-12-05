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

from carbon.pydantic.organization_user_files_to_sync_filters import OrganizationUserFilesToSyncFilters

class ModifyColdStorageParametersQueryInput(BaseModel):
    filters: typing.Optional[OrganizationUserFilesToSyncFilters] = Field(None, alias='filters')

    enable_cold_storage: typing.Optional[typing.Optional[bool]] = Field(None, alias='enable_cold_storage')

    hot_storage_time_to_live: typing.Optional[typing.Optional[int]] = Field(None, alias='hot_storage_time_to_live')

    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True
    )
