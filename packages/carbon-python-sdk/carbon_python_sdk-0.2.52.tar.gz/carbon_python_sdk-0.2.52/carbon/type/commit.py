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

from carbon.type.commit_user_nullable import CommitUserNullable
from carbon.type.tree import Tree

class RequiredCommit(TypedDict):
    author: typing.Optional[CommitUserNullable]

    committer: typing.Optional[CommitUserNullable]

    message: str

    tree: Tree

    url: str

    comment_count: int

class OptionalCommit(TypedDict, total=False):
    pass

class Commit(RequiredCommit, OptionalCommit):
    pass
