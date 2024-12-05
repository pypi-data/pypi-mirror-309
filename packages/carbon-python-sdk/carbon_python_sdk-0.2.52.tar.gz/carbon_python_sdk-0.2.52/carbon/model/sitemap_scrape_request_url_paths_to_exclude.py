# coding: utf-8

"""
    Carbon

    Connect external data to LLMs, no matter the source.

    The version of the OpenAPI document: 1.0.0
    Generated by: https://konfigthis.com
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from carbon import schemas  # noqa: F401


class SitemapScrapeRequestUrlPathsToExclude(
    schemas.ListBase,
    schemas.NoneBase,
    schemas.Schema,
    schemas.NoneTupleMixin
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    URL subpaths or directories that you want to exclude. For example if you want to exclude
        URLs that start with /questions in stackoverflow.com, you will add /questions/ in this input
    """


    class MetaOapg:
        items = schemas.StrSchema
        max_items = 10


    def __new__(
        cls,
        *args: typing.Union[list, tuple, None, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'SitemapScrapeRequestUrlPathsToExclude':
        return super().__new__(
            cls,
            *args,
            _configuration=_configuration,
        )
