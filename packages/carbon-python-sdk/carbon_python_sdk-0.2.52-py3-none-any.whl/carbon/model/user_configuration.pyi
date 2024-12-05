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


class UserConfiguration(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        
        class properties:
            
            
            class auto_sync_enabled_sources(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    
                    
                    class any_of_0(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            
                            @staticmethod
                            def items() -> typing.Type['DataSourceType']:
                                return DataSourceType
                    
                        def __new__(
                            cls,
                            arg: typing.Union[typing.Tuple['DataSourceType'], typing.List['DataSourceType']],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'any_of_0':
                            return super().__new__(
                                cls,
                                arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> 'DataSourceType':
                            return super().__getitem__(i)
                    
                    @classmethod
                    @functools.lru_cache()
                    def any_of(cls):
                        # we need this here to make our import statements work
                        # we must store _composed_schemas in here so the code is only run
                        # when we invoke this method. If we kept this at the class
                        # level we would get an error because the class level
                        # code would be run when this module is imported, and these composed
                        # classes don't exist yet because their module has not finished
                        # loading
                        return [
                            cls.any_of_0,
                            DataSourceExtendedInput,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'auto_sync_enabled_sources':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class max_files(
                schemas.IntBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'max_files':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class max_files_per_upload(
                schemas.IntBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'max_files_per_upload':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class max_characters(
                schemas.IntBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'max_characters':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class max_characters_per_file(
                schemas.IntBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'max_characters_per_file':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class max_characters_per_upload(
                schemas.IntBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'max_characters_per_upload':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class auto_sync_interval(
                schemas.IntBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'auto_sync_interval':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "auto_sync_enabled_sources": auto_sync_enabled_sources,
                "max_files": max_files,
                "max_files_per_upload": max_files_per_upload,
                "max_characters": max_characters,
                "max_characters_per_file": max_characters_per_file,
                "max_characters_per_upload": max_characters_per_upload,
                "auto_sync_interval": auto_sync_interval,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["auto_sync_enabled_sources"]) -> MetaOapg.properties.auto_sync_enabled_sources: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_files"]) -> MetaOapg.properties.max_files: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_files_per_upload"]) -> MetaOapg.properties.max_files_per_upload: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_characters"]) -> MetaOapg.properties.max_characters: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_characters_per_file"]) -> MetaOapg.properties.max_characters_per_file: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_characters_per_upload"]) -> MetaOapg.properties.max_characters_per_upload: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["auto_sync_interval"]) -> MetaOapg.properties.auto_sync_interval: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["auto_sync_enabled_sources", "max_files", "max_files_per_upload", "max_characters", "max_characters_per_file", "max_characters_per_upload", "auto_sync_interval", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["auto_sync_enabled_sources"]) -> typing.Union[MetaOapg.properties.auto_sync_enabled_sources, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_files"]) -> typing.Union[MetaOapg.properties.max_files, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_files_per_upload"]) -> typing.Union[MetaOapg.properties.max_files_per_upload, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_characters"]) -> typing.Union[MetaOapg.properties.max_characters, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_characters_per_file"]) -> typing.Union[MetaOapg.properties.max_characters_per_file, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_characters_per_upload"]) -> typing.Union[MetaOapg.properties.max_characters_per_upload, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["auto_sync_interval"]) -> typing.Union[MetaOapg.properties.auto_sync_interval, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["auto_sync_enabled_sources", "max_files", "max_files_per_upload", "max_characters", "max_characters_per_file", "max_characters_per_upload", "auto_sync_interval", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        auto_sync_enabled_sources: typing.Union[MetaOapg.properties.auto_sync_enabled_sources, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        max_files: typing.Union[MetaOapg.properties.max_files, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_files_per_upload: typing.Union[MetaOapg.properties.max_files_per_upload, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_characters: typing.Union[MetaOapg.properties.max_characters, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_characters_per_file: typing.Union[MetaOapg.properties.max_characters_per_file, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_characters_per_upload: typing.Union[MetaOapg.properties.max_characters_per_upload, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        auto_sync_interval: typing.Union[MetaOapg.properties.auto_sync_interval, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'UserConfiguration':
        return super().__new__(
            cls,
            *args,
            auto_sync_enabled_sources=auto_sync_enabled_sources,
            max_files=max_files,
            max_files_per_upload=max_files_per_upload,
            max_characters=max_characters,
            max_characters_per_file=max_characters_per_file,
            max_characters_per_upload=max_characters_per_upload,
            auto_sync_interval=auto_sync_interval,
            _configuration=_configuration,
            **kwargs,
        )

from carbon.model.data_source_extended_input import DataSourceExtendedInput
from carbon.model.data_source_type import DataSourceType
