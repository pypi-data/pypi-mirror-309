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


class Webhook(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        required = {
            "signing_key",
            "updated_at",
            "organization_id",
            "created_at",
            "id",
            "url",
            "status",
        }
        
        class properties:
            id = schemas.IntSchema
            organization_id = schemas.IntSchema
            url = schemas.StrSchema
            signing_key = schemas.StrSchema
        
            @staticmethod
            def status() -> typing.Type['WebhookStatus']:
                return WebhookStatus
            created_at = schemas.DateTimeSchema
            updated_at = schemas.DateTimeSchema
            
            
            class status_reason(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'status_reason':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "id": id,
                "organization_id": organization_id,
                "url": url,
                "signing_key": signing_key,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
                "status_reason": status_reason,
            }
    
    signing_key: MetaOapg.properties.signing_key
    updated_at: MetaOapg.properties.updated_at
    organization_id: MetaOapg.properties.organization_id
    created_at: MetaOapg.properties.created_at
    id: MetaOapg.properties.id
    url: MetaOapg.properties.url
    status: 'WebhookStatus'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["organization_id"]) -> MetaOapg.properties.organization_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["url"]) -> MetaOapg.properties.url: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["signing_key"]) -> MetaOapg.properties.signing_key: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> 'WebhookStatus': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created_at"]) -> MetaOapg.properties.created_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updated_at"]) -> MetaOapg.properties.updated_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status_reason"]) -> MetaOapg.properties.status_reason: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "organization_id", "url", "signing_key", "status", "created_at", "updated_at", "status_reason", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["organization_id"]) -> MetaOapg.properties.organization_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["url"]) -> MetaOapg.properties.url: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["signing_key"]) -> MetaOapg.properties.signing_key: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> 'WebhookStatus': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created_at"]) -> MetaOapg.properties.created_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updated_at"]) -> MetaOapg.properties.updated_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status_reason"]) -> typing.Union[MetaOapg.properties.status_reason, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "organization_id", "url", "signing_key", "status", "created_at", "updated_at", "status_reason", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        signing_key: typing.Union[MetaOapg.properties.signing_key, str, ],
        updated_at: typing.Union[MetaOapg.properties.updated_at, str, datetime, ],
        organization_id: typing.Union[MetaOapg.properties.organization_id, decimal.Decimal, int, ],
        created_at: typing.Union[MetaOapg.properties.created_at, str, datetime, ],
        id: typing.Union[MetaOapg.properties.id, decimal.Decimal, int, ],
        url: typing.Union[MetaOapg.properties.url, str, ],
        status: 'WebhookStatus',
        status_reason: typing.Union[MetaOapg.properties.status_reason, None, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Webhook':
        return super().__new__(
            cls,
            *args,
            signing_key=signing_key,
            updated_at=updated_at,
            organization_id=organization_id,
            created_at=created_at,
            id=id,
            url=url,
            status=status,
            status_reason=status_reason,
            _configuration=_configuration,
            **kwargs,
        )

from carbon.model.webhook_status import WebhookStatus
