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


class OrganizationUserDataSourceFilters(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        
        class properties:
            
            
            class tags(
                schemas.DictBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneFrozenDictMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'tags':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
        
            @staticmethod
            def source() -> typing.Type['DataSourceTypeNullable']:
                return DataSourceTypeNullable
        
            @staticmethod
            def ids() -> typing.Type['OrganizationUserDataSourceFiltersIds']:
                return OrganizationUserDataSourceFiltersIds
            
            
            class revoked_access(
                schemas.BoolBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneBoolMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, bool, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'revoked_access':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "tags": tags,
                "source": source,
                "ids": ids,
                "revoked_access": revoked_access,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tags"]) -> MetaOapg.properties.tags: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["source"]) -> 'DataSourceTypeNullable': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["ids"]) -> 'OrganizationUserDataSourceFiltersIds': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["revoked_access"]) -> MetaOapg.properties.revoked_access: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["tags", "source", "ids", "revoked_access", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tags"]) -> typing.Union[MetaOapg.properties.tags, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["source"]) -> typing.Union['DataSourceTypeNullable', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["ids"]) -> typing.Union['OrganizationUserDataSourceFiltersIds', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["revoked_access"]) -> typing.Union[MetaOapg.properties.revoked_access, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["tags", "source", "ids", "revoked_access", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        tags: typing.Union[MetaOapg.properties.tags, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        source: typing.Union['DataSourceTypeNullable', schemas.Unset] = schemas.unset,
        ids: typing.Union['OrganizationUserDataSourceFiltersIds', schemas.Unset] = schemas.unset,
        revoked_access: typing.Union[MetaOapg.properties.revoked_access, None, bool, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'OrganizationUserDataSourceFilters':
        return super().__new__(
            cls,
            *args,
            tags=tags,
            source=source,
            ids=ids,
            revoked_access=revoked_access,
            _configuration=_configuration,
            **kwargs,
        )

from carbon.model.data_source_type_nullable import DataSourceTypeNullable
from carbon.model.organization_user_data_source_filters_ids import OrganizationUserDataSourceFiltersIds
