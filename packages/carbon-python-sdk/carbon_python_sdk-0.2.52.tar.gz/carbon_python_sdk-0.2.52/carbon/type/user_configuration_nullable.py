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

from carbon.type.data_source_extended_input import DataSourceExtendedInput
from carbon.type.data_source_type import DataSourceType

class RequiredUserConfigurationNullable(TypedDict):
    pass

class OptionalUserConfigurationNullable(TypedDict, total=False):
    # List of data source types to enable auto sync for. Empty array will remove all sources          and the string \"ALL\" will enable it for all data sources
    auto_sync_enabled_sources: typing.Union[typing.List[DataSourceType], DataSourceExtendedInput]

    # Custom file upload limit for the user over *all* user's files across all uploads.          If set, then the user will not be allowed to upload more files than this limit. If not set, or if set to -1,         then the user will have no limit.
    max_files: typing.Optional[int]

    # Custom file upload limit for the user across a single upload.         If set, then the user will not be allowed to upload more files than this limit in a single upload. If not set,         or if set to -1, then the user will have no limit.
    max_files_per_upload: typing.Optional[int]

    # Custom character upload limit for the user over *all* user's files across all uploads.          If set, then the user will not be allowed to upload more characters than this limit. If not set, or if set to -1,         then the user will have no limit.
    max_characters: typing.Optional[int]

    # A single file upload from the user can not exceed this character limit.         If set, then the file will not be synced if it exceeds this limit. If not set, or if set to -1, then the          user will have no limit.
    max_characters_per_file: typing.Optional[int]

    # Custom character upload limit for the user across a single upload.         If set, then the user won't be able to sync more than this many characters in one upload.          If not set, or if set to -1, then the user will have no limit.
    max_characters_per_upload: typing.Optional[int]

    # The interval in hours at which the user's data sources should be synced. If not set or set to -1,          the user will be synced at the organization level interval or default interval if that is also not set.          Must be one of [3, 6, 12, 24]
    auto_sync_interval: typing.Optional[int]

class UserConfigurationNullable(RequiredUserConfigurationNullable, OptionalUserConfigurationNullable):
    pass
