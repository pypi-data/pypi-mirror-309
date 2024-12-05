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


class ConnectDataSourceInput(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        required = {
            "authentication",
        }
        
        class properties:
            
            
            class authentication(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    
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
                            OAuthAuthentication,
                            NotionAuthentication,
                            OneDriveAuthentication,
                            SharepointAuthentication,
                            ConfluenceAuthentication,
                            ZendeskAuthentication,
                            ZoteroAuthentication,
                            GitbookAuthetication,
                            SalesforceAuthentication,
                            FreskdeskAuthentication,
                            S3Authentication,
                            AzureBlobStorageAuthentication,
                            GithubAuthentication,
                            ServiceNowAuthentication,
                            GuruAuthentication,
                            GongAuthentication,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'authentication':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
        
            @staticmethod
            def sync_options() -> typing.Type['SyncOptions']:
                return SyncOptions
            __annotations__ = {
                "authentication": authentication,
                "sync_options": sync_options,
            }
    
    authentication: MetaOapg.properties.authentication
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["authentication"]) -> MetaOapg.properties.authentication: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["sync_options"]) -> 'SyncOptions': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["authentication", "sync_options", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["authentication"]) -> MetaOapg.properties.authentication: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["sync_options"]) -> typing.Union['SyncOptions', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["authentication", "sync_options", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        authentication: typing.Union[MetaOapg.properties.authentication, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        sync_options: typing.Union['SyncOptions', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ConnectDataSourceInput':
        return super().__new__(
            cls,
            *args,
            authentication=authentication,
            sync_options=sync_options,
            _configuration=_configuration,
            **kwargs,
        )

from carbon.model.azure_blob_storage_authentication import AzureBlobStorageAuthentication
from carbon.model.confluence_authentication import ConfluenceAuthentication
from carbon.model.freskdesk_authentication import FreskdeskAuthentication
from carbon.model.gitbook_authetication import GitbookAuthetication
from carbon.model.github_authentication import GithubAuthentication
from carbon.model.gong_authentication import GongAuthentication
from carbon.model.guru_authentication import GuruAuthentication
from carbon.model.notion_authentication import NotionAuthentication
from carbon.model.o_auth_authentication import OAuthAuthentication
from carbon.model.one_drive_authentication import OneDriveAuthentication
from carbon.model.s3_authentication import S3Authentication
from carbon.model.salesforce_authentication import SalesforceAuthentication
from carbon.model.service_now_authentication import ServiceNowAuthentication
from carbon.model.sharepoint_authentication import SharepointAuthentication
from carbon.model.sync_options import SyncOptions
from carbon.model.zendesk_authentication import ZendeskAuthentication
from carbon.model.zotero_authentication import ZoteroAuthentication
