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

from carbon.type.pr_commit import PRCommit

class RequiredCommitsResponse(TypedDict):
    data: typing.List[PRCommit]

    next_cursor: typing.Optional[str]

class OptionalCommitsResponse(TypedDict, total=False):
    pass

class CommitsResponse(RequiredCommitsResponse, OptionalCommitsResponse):
    pass
