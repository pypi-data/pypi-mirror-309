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

from carbon.type.list_items_filters_external_ids import ListItemsFiltersExternalIds
from carbon.type.list_items_filters_ids import ListItemsFiltersIds
from carbon.type.list_items_filters_item_types import ListItemsFiltersItemTypes
from carbon.type.storage_file_formats import StorageFileFormats

class RequiredListItemsFilters(TypedDict):
    pass

class OptionalListItemsFilters(TypedDict, total=False):
    external_ids: typing.Optional[ListItemsFiltersExternalIds]

    ids: typing.Optional[ListItemsFiltersIds]

    name: typing.Optional[str]

    root_files_only: typing.Optional[bool]

    file_formats: typing.Optional[typing.List[StorageFileFormats]]

    item_types: typing.Optional[ListItemsFiltersItemTypes]

class ListItemsFilters(RequiredListItemsFilters, OptionalListItemsFilters):
    pass
