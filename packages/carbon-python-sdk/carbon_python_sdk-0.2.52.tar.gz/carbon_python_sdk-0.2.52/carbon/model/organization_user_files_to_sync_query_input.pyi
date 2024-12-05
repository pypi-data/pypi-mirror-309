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


class OrganizationUserFilesToSyncQueryInput(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        
        class properties:
        
            @staticmethod
            def pagination() -> typing.Type['Pagination']:
                return Pagination
        
            @staticmethod
            def order_by() -> typing.Type['OrganizationUserFilesToSyncOrderByTypes']:
                return OrganizationUserFilesToSyncOrderByTypes
        
            @staticmethod
            def order_dir() -> typing.Type['OrderDir']:
                return OrderDir
        
            @staticmethod
            def filters() -> typing.Type['OrganizationUserFilesToSyncFilters']:
                return OrganizationUserFilesToSyncFilters
            
            
            class include_raw_file(
                schemas.BoolBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneBoolMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, bool, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'include_raw_file':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class include_parsed_text_file(
                schemas.BoolBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneBoolMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, bool, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'include_parsed_text_file':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class include_additional_files(
                schemas.BoolBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneBoolMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, bool, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'include_additional_files':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            presigned_url_expiry_time_seconds = schemas.IntSchema
            __annotations__ = {
                "pagination": pagination,
                "order_by": order_by,
                "order_dir": order_dir,
                "filters": filters,
                "include_raw_file": include_raw_file,
                "include_parsed_text_file": include_parsed_text_file,
                "include_additional_files": include_additional_files,
                "presigned_url_expiry_time_seconds": presigned_url_expiry_time_seconds,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pagination"]) -> 'Pagination': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["order_by"]) -> 'OrganizationUserFilesToSyncOrderByTypes': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["order_dir"]) -> 'OrderDir': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["filters"]) -> 'OrganizationUserFilesToSyncFilters': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["include_raw_file"]) -> MetaOapg.properties.include_raw_file: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["include_parsed_text_file"]) -> MetaOapg.properties.include_parsed_text_file: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["include_additional_files"]) -> MetaOapg.properties.include_additional_files: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["presigned_url_expiry_time_seconds"]) -> MetaOapg.properties.presigned_url_expiry_time_seconds: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["pagination", "order_by", "order_dir", "filters", "include_raw_file", "include_parsed_text_file", "include_additional_files", "presigned_url_expiry_time_seconds", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pagination"]) -> typing.Union['Pagination', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["order_by"]) -> typing.Union['OrganizationUserFilesToSyncOrderByTypes', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["order_dir"]) -> typing.Union['OrderDir', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["filters"]) -> typing.Union['OrganizationUserFilesToSyncFilters', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["include_raw_file"]) -> typing.Union[MetaOapg.properties.include_raw_file, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["include_parsed_text_file"]) -> typing.Union[MetaOapg.properties.include_parsed_text_file, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["include_additional_files"]) -> typing.Union[MetaOapg.properties.include_additional_files, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["presigned_url_expiry_time_seconds"]) -> typing.Union[MetaOapg.properties.presigned_url_expiry_time_seconds, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["pagination", "order_by", "order_dir", "filters", "include_raw_file", "include_parsed_text_file", "include_additional_files", "presigned_url_expiry_time_seconds", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        pagination: typing.Union['Pagination', schemas.Unset] = schemas.unset,
        order_by: typing.Union['OrganizationUserFilesToSyncOrderByTypes', schemas.Unset] = schemas.unset,
        order_dir: typing.Union['OrderDir', schemas.Unset] = schemas.unset,
        filters: typing.Union['OrganizationUserFilesToSyncFilters', schemas.Unset] = schemas.unset,
        include_raw_file: typing.Union[MetaOapg.properties.include_raw_file, None, bool, schemas.Unset] = schemas.unset,
        include_parsed_text_file: typing.Union[MetaOapg.properties.include_parsed_text_file, None, bool, schemas.Unset] = schemas.unset,
        include_additional_files: typing.Union[MetaOapg.properties.include_additional_files, None, bool, schemas.Unset] = schemas.unset,
        presigned_url_expiry_time_seconds: typing.Union[MetaOapg.properties.presigned_url_expiry_time_seconds, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'OrganizationUserFilesToSyncQueryInput':
        return super().__new__(
            cls,
            *args,
            pagination=pagination,
            order_by=order_by,
            order_dir=order_dir,
            filters=filters,
            include_raw_file=include_raw_file,
            include_parsed_text_file=include_parsed_text_file,
            include_additional_files=include_additional_files,
            presigned_url_expiry_time_seconds=presigned_url_expiry_time_seconds,
            _configuration=_configuration,
            **kwargs,
        )

from carbon.model.order_dir import OrderDir
from carbon.model.organization_user_files_to_sync_filters import OrganizationUserFilesToSyncFilters
from carbon.model.organization_user_files_to_sync_order_by_types import OrganizationUserFilesToSyncOrderByTypes
from carbon.model.pagination import Pagination
