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

from carbon.type.oauth_based_connectors import OauthBasedConnectors
from carbon.type.white_label_filters_ids import WhiteLabelFiltersIds

class RequiredWhiteLabelFilters(TypedDict):
    pass

class OptionalWhiteLabelFilters(TypedDict, total=False):
    ids: typing.Optional[WhiteLabelFiltersIds]

    data_source_type: typing.Optional[typing.List[OauthBasedConnectors]]

class WhiteLabelFilters(RequiredWhiteLabelFilters, OptionalWhiteLabelFilters):
    pass
