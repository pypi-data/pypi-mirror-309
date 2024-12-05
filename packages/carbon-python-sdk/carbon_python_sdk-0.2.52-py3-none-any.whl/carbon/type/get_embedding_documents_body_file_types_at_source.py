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

from carbon.type.helpdesk_file_types import HelpdeskFileTypes
from carbon.type.service_now_file_types import ServiceNowFileTypes

GetEmbeddingDocumentsBodyFileTypesAtSource = typing.Optional[typing.List[typing.Union[HelpdeskFileTypes, ServiceNowFileTypes]]]
