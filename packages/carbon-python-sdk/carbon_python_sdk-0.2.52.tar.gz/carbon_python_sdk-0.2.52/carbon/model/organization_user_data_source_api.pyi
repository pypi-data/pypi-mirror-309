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


class OrganizationUserDataSourceAPI(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        required = {
            "last_synced_at",
            "revoked_access",
            "created_at",
            "data_source_type",
            "data_source_metadata",
            "organization_supplied_user_id",
            "tags",
            "token",
            "updated_at",
            "files_synced_at",
            "source_items_synced_at",
            "enable_auto_sync",
            "organization_id",
            "organization_user_id",
            "last_sync_action",
            "sync_status",
            "id",
            "data_source_external_id",
        }
        
        class properties:
            tags = schemas.DictSchema
            id = schemas.IntSchema
            
            
            class data_source_external_id(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'data_source_external_id':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
        
            @staticmethod
            def data_source_type() -> typing.Type['DataSourceType']:
                return DataSourceType
            
            
            class token(
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
                ) -> 'token':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
        
            @staticmethod
            def sync_status() -> typing.Type['DataSourceSyncStatuses']:
                return DataSourceSyncStatuses
            
            
            class source_items_synced_at(
                schemas.DateTimeBase,
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                class MetaOapg:
                    format = 'date-time'
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, datetime, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'source_items_synced_at':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            organization_user_id = schemas.IntSchema
            organization_id = schemas.IntSchema
            organization_supplied_user_id = schemas.StrSchema
            revoked_access = schemas.BoolSchema
            last_synced_at = schemas.DateTimeSchema
        
            @staticmethod
            def last_sync_action() -> typing.Type['DataSourceLastSyncActions']:
                return DataSourceLastSyncActions
            
            
            class enable_auto_sync(
                schemas.BoolBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneBoolMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, bool, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'enable_auto_sync':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            created_at = schemas.DateTimeSchema
            updated_at = schemas.DateTimeSchema
            
            
            class files_synced_at(
                schemas.DateTimeBase,
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                class MetaOapg:
                    format = 'date-time'
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, datetime, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'files_synced_at':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            data_source_metadata = schemas.DictSchema
            __annotations__ = {
                "tags": tags,
                "id": id,
                "data_source_external_id": data_source_external_id,
                "data_source_type": data_source_type,
                "token": token,
                "sync_status": sync_status,
                "source_items_synced_at": source_items_synced_at,
                "organization_user_id": organization_user_id,
                "organization_id": organization_id,
                "organization_supplied_user_id": organization_supplied_user_id,
                "revoked_access": revoked_access,
                "last_synced_at": last_synced_at,
                "last_sync_action": last_sync_action,
                "enable_auto_sync": enable_auto_sync,
                "created_at": created_at,
                "updated_at": updated_at,
                "files_synced_at": files_synced_at,
                "data_source_metadata": data_source_metadata,
            }
    
    last_synced_at: MetaOapg.properties.last_synced_at
    revoked_access: MetaOapg.properties.revoked_access
    created_at: MetaOapg.properties.created_at
    data_source_type: 'DataSourceType'
    data_source_metadata: MetaOapg.properties.data_source_metadata
    organization_supplied_user_id: MetaOapg.properties.organization_supplied_user_id
    tags: MetaOapg.properties.tags
    token: MetaOapg.properties.token
    updated_at: MetaOapg.properties.updated_at
    files_synced_at: MetaOapg.properties.files_synced_at
    source_items_synced_at: MetaOapg.properties.source_items_synced_at
    enable_auto_sync: MetaOapg.properties.enable_auto_sync
    organization_id: MetaOapg.properties.organization_id
    organization_user_id: MetaOapg.properties.organization_user_id
    last_sync_action: 'DataSourceLastSyncActions'
    sync_status: 'DataSourceSyncStatuses'
    id: MetaOapg.properties.id
    data_source_external_id: MetaOapg.properties.data_source_external_id
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tags"]) -> MetaOapg.properties.tags: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["data_source_external_id"]) -> MetaOapg.properties.data_source_external_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["data_source_type"]) -> 'DataSourceType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["token"]) -> MetaOapg.properties.token: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["sync_status"]) -> 'DataSourceSyncStatuses': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["source_items_synced_at"]) -> MetaOapg.properties.source_items_synced_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["organization_user_id"]) -> MetaOapg.properties.organization_user_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["organization_id"]) -> MetaOapg.properties.organization_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["organization_supplied_user_id"]) -> MetaOapg.properties.organization_supplied_user_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["revoked_access"]) -> MetaOapg.properties.revoked_access: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_synced_at"]) -> MetaOapg.properties.last_synced_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_sync_action"]) -> 'DataSourceLastSyncActions': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["enable_auto_sync"]) -> MetaOapg.properties.enable_auto_sync: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created_at"]) -> MetaOapg.properties.created_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updated_at"]) -> MetaOapg.properties.updated_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["files_synced_at"]) -> MetaOapg.properties.files_synced_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["data_source_metadata"]) -> MetaOapg.properties.data_source_metadata: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["tags", "id", "data_source_external_id", "data_source_type", "token", "sync_status", "source_items_synced_at", "organization_user_id", "organization_id", "organization_supplied_user_id", "revoked_access", "last_synced_at", "last_sync_action", "enable_auto_sync", "created_at", "updated_at", "files_synced_at", "data_source_metadata", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tags"]) -> MetaOapg.properties.tags: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["data_source_external_id"]) -> MetaOapg.properties.data_source_external_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["data_source_type"]) -> 'DataSourceType': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["token"]) -> MetaOapg.properties.token: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["sync_status"]) -> 'DataSourceSyncStatuses': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["source_items_synced_at"]) -> MetaOapg.properties.source_items_synced_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["organization_user_id"]) -> MetaOapg.properties.organization_user_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["organization_id"]) -> MetaOapg.properties.organization_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["organization_supplied_user_id"]) -> MetaOapg.properties.organization_supplied_user_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["revoked_access"]) -> MetaOapg.properties.revoked_access: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_synced_at"]) -> MetaOapg.properties.last_synced_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_sync_action"]) -> 'DataSourceLastSyncActions': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["enable_auto_sync"]) -> MetaOapg.properties.enable_auto_sync: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created_at"]) -> MetaOapg.properties.created_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updated_at"]) -> MetaOapg.properties.updated_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["files_synced_at"]) -> MetaOapg.properties.files_synced_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["data_source_metadata"]) -> MetaOapg.properties.data_source_metadata: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["tags", "id", "data_source_external_id", "data_source_type", "token", "sync_status", "source_items_synced_at", "organization_user_id", "organization_id", "organization_supplied_user_id", "revoked_access", "last_synced_at", "last_sync_action", "enable_auto_sync", "created_at", "updated_at", "files_synced_at", "data_source_metadata", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        last_synced_at: typing.Union[MetaOapg.properties.last_synced_at, str, datetime, ],
        revoked_access: typing.Union[MetaOapg.properties.revoked_access, bool, ],
        created_at: typing.Union[MetaOapg.properties.created_at, str, datetime, ],
        data_source_type: 'DataSourceType',
        data_source_metadata: typing.Union[MetaOapg.properties.data_source_metadata, dict, frozendict.frozendict, ],
        organization_supplied_user_id: typing.Union[MetaOapg.properties.organization_supplied_user_id, str, ],
        tags: typing.Union[MetaOapg.properties.tags, dict, frozendict.frozendict, ],
        token: typing.Union[MetaOapg.properties.token, dict, frozendict.frozendict, None, ],
        updated_at: typing.Union[MetaOapg.properties.updated_at, str, datetime, ],
        files_synced_at: typing.Union[MetaOapg.properties.files_synced_at, None, str, datetime, ],
        source_items_synced_at: typing.Union[MetaOapg.properties.source_items_synced_at, None, str, datetime, ],
        enable_auto_sync: typing.Union[MetaOapg.properties.enable_auto_sync, None, bool, ],
        organization_id: typing.Union[MetaOapg.properties.organization_id, decimal.Decimal, int, ],
        organization_user_id: typing.Union[MetaOapg.properties.organization_user_id, decimal.Decimal, int, ],
        last_sync_action: 'DataSourceLastSyncActions',
        sync_status: 'DataSourceSyncStatuses',
        id: typing.Union[MetaOapg.properties.id, decimal.Decimal, int, ],
        data_source_external_id: typing.Union[MetaOapg.properties.data_source_external_id, None, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'OrganizationUserDataSourceAPI':
        return super().__new__(
            cls,
            *args,
            last_synced_at=last_synced_at,
            revoked_access=revoked_access,
            created_at=created_at,
            data_source_type=data_source_type,
            data_source_metadata=data_source_metadata,
            organization_supplied_user_id=organization_supplied_user_id,
            tags=tags,
            token=token,
            updated_at=updated_at,
            files_synced_at=files_synced_at,
            source_items_synced_at=source_items_synced_at,
            enable_auto_sync=enable_auto_sync,
            organization_id=organization_id,
            organization_user_id=organization_user_id,
            last_sync_action=last_sync_action,
            sync_status=sync_status,
            id=id,
            data_source_external_id=data_source_external_id,
            _configuration=_configuration,
            **kwargs,
        )

from carbon.model.data_source_last_sync_actions import DataSourceLastSyncActions
from carbon.model.data_source_sync_statuses import DataSourceSyncStatuses
from carbon.model.data_source_type import DataSourceType
