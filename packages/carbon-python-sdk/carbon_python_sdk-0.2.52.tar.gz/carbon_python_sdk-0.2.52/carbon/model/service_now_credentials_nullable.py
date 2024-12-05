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


class ServiceNowCredentialsNullable(
    schemas.DictBase,
    schemas.NoneBase,
    schemas.Schema,
    schemas.NoneFrozenDictMixin
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    ServiceNow credentials required to connect a ServiceNow account. The instance_subdomain can be extracted from
        the url of the instance url which takes the form of "<instance-subdomain>.service-now.com". The client_id and client_secret are
        values generated by creating a new OAuth API Integration in ServiceNow. When creating the OAuth API Integration, the redirect
        uri must be "https://api.carbon.ai/integrations/servicenow" or a similar one using a CNAME.
    """


    class MetaOapg:
        required = {
            "instance_subdomain",
            "client_secret",
            "redirect_uri",
            "client_id",
        }
        
        class properties:
            instance_subdomain = schemas.StrSchema
            client_id = schemas.StrSchema
            client_secret = schemas.StrSchema
            redirect_uri = schemas.StrSchema
            __annotations__ = {
                "instance_subdomain": instance_subdomain,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
            }

    
    instance_subdomain: MetaOapg.properties.instance_subdomain
    client_secret: MetaOapg.properties.client_secret
    redirect_uri: MetaOapg.properties.redirect_uri
    client_id: MetaOapg.properties.client_id
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["instance_subdomain"]) -> MetaOapg.properties.instance_subdomain: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["client_id"]) -> MetaOapg.properties.client_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["client_secret"]) -> MetaOapg.properties.client_secret: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["redirect_uri"]) -> MetaOapg.properties.redirect_uri: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["instance_subdomain", "client_id", "client_secret", "redirect_uri", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["instance_subdomain"]) -> MetaOapg.properties.instance_subdomain: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["client_id"]) -> MetaOapg.properties.client_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["client_secret"]) -> MetaOapg.properties.client_secret: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["redirect_uri"]) -> MetaOapg.properties.redirect_uri: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["instance_subdomain", "client_id", "client_secret", "redirect_uri", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, None, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ServiceNowCredentialsNullable':
        return super().__new__(
            cls,
            *args,
            _configuration=_configuration,
            **kwargs,
        )
