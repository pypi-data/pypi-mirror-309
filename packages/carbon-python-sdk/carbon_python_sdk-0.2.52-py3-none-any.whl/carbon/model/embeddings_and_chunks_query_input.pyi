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


class EmbeddingsAndChunksQueryInput(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        required = {
            "filters",
        }
        
        class properties:
        
            @staticmethod
            def filters() -> typing.Type['EmbeddingsAndChunksFilters']:
                return EmbeddingsAndChunksFilters
        
            @staticmethod
            def pagination() -> typing.Type['Pagination']:
                return Pagination
        
            @staticmethod
            def order_by() -> typing.Type['EmbeddingsAndChunksOrderByColumns']:
                return EmbeddingsAndChunksOrderByColumns
        
            @staticmethod
            def order_dir() -> typing.Type['OrderDir']:
                return OrderDir
            include_vectors = schemas.BoolSchema
            __annotations__ = {
                "filters": filters,
                "pagination": pagination,
                "order_by": order_by,
                "order_dir": order_dir,
                "include_vectors": include_vectors,
            }
    
    filters: 'EmbeddingsAndChunksFilters'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["filters"]) -> 'EmbeddingsAndChunksFilters': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pagination"]) -> 'Pagination': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["order_by"]) -> 'EmbeddingsAndChunksOrderByColumns': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["order_dir"]) -> 'OrderDir': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["include_vectors"]) -> MetaOapg.properties.include_vectors: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["filters", "pagination", "order_by", "order_dir", "include_vectors", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["filters"]) -> 'EmbeddingsAndChunksFilters': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pagination"]) -> typing.Union['Pagination', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["order_by"]) -> typing.Union['EmbeddingsAndChunksOrderByColumns', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["order_dir"]) -> typing.Union['OrderDir', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["include_vectors"]) -> typing.Union[MetaOapg.properties.include_vectors, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["filters", "pagination", "order_by", "order_dir", "include_vectors", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        filters: 'EmbeddingsAndChunksFilters',
        pagination: typing.Union['Pagination', schemas.Unset] = schemas.unset,
        order_by: typing.Union['EmbeddingsAndChunksOrderByColumns', schemas.Unset] = schemas.unset,
        order_dir: typing.Union['OrderDir', schemas.Unset] = schemas.unset,
        include_vectors: typing.Union[MetaOapg.properties.include_vectors, bool, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'EmbeddingsAndChunksQueryInput':
        return super().__new__(
            cls,
            *args,
            filters=filters,
            pagination=pagination,
            order_by=order_by,
            order_dir=order_dir,
            include_vectors=include_vectors,
            _configuration=_configuration,
            **kwargs,
        )

from carbon.model.embeddings_and_chunks_filters import EmbeddingsAndChunksFilters
from carbon.model.embeddings_and_chunks_order_by_columns import EmbeddingsAndChunksOrderByColumns
from carbon.model.order_dir import OrderDir
from carbon.model.pagination import Pagination
