# coding: utf-8

"""
    Carbon

    Connect external data to LLMs, no matter the source.

    The version of the OpenAPI document: 1.0.0
    Generated by: https://konfigthis.com
"""

from dataclasses import dataclass
import typing_extensions
import urllib3
from pydantic import RootModel
from carbon.request_before_hook import request_before_hook
import json
from urllib3._collections import HTTPHeaderDict

from carbon.api_response import AsyncGeneratorResponse
from carbon import api_client, exceptions
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

from carbon.model.one_drive_authentication import OneDriveAuthentication as OneDriveAuthenticationSchema
from carbon.model.connect_data_source_input import ConnectDataSourceInput as ConnectDataSourceInputSchema
from carbon.model.guru_authentication import GuruAuthentication as GuruAuthenticationSchema
from carbon.model.freskdesk_authentication import FreskdeskAuthentication as FreskdeskAuthenticationSchema
from carbon.model.connect_data_source_response import ConnectDataSourceResponse as ConnectDataSourceResponseSchema
from carbon.model.zendesk_authentication import ZendeskAuthentication as ZendeskAuthenticationSchema
from carbon.model.o_auth_authentication import OAuthAuthentication as OAuthAuthenticationSchema
from carbon.model.azure_blob_storage_authentication import AzureBlobStorageAuthentication as AzureBlobStorageAuthenticationSchema
from carbon.model.confluence_authentication import ConfluenceAuthentication as ConfluenceAuthenticationSchema
from carbon.model.sync_options import SyncOptions as SyncOptionsSchema
from carbon.model.service_now_authentication import ServiceNowAuthentication as ServiceNowAuthenticationSchema
from carbon.model.gitbook_authetication import GitbookAuthetication as GitbookAutheticationSchema
from carbon.model.http_validation_error import HTTPValidationError as HTTPValidationErrorSchema
from carbon.model.s3_authentication import S3Authentication as S3AuthenticationSchema
from carbon.model.salesforce_authentication import SalesforceAuthentication as SalesforceAuthenticationSchema
from carbon.model.notion_authentication import NotionAuthentication as NotionAuthenticationSchema
from carbon.model.sharepoint_authentication import SharepointAuthentication as SharepointAuthenticationSchema
from carbon.model.zotero_authentication import ZoteroAuthentication as ZoteroAuthenticationSchema
from carbon.model.gong_authentication import GongAuthentication as GongAuthenticationSchema
from carbon.model.github_authentication import GithubAuthentication as GithubAuthenticationSchema

from carbon.type.salesforce_authentication import SalesforceAuthentication
from carbon.type.freskdesk_authentication import FreskdeskAuthentication
from carbon.type.connect_data_source_response import ConnectDataSourceResponse
from carbon.type.gitbook_authetication import GitbookAuthetication
from carbon.type.service_now_authentication import ServiceNowAuthentication
from carbon.type.notion_authentication import NotionAuthentication
from carbon.type.zotero_authentication import ZoteroAuthentication
from carbon.type.sharepoint_authentication import SharepointAuthentication
from carbon.type.github_authentication import GithubAuthentication
from carbon.type.guru_authentication import GuruAuthentication
from carbon.type.zendesk_authentication import ZendeskAuthentication
from carbon.type.http_validation_error import HTTPValidationError
from carbon.type.o_auth_authentication import OAuthAuthentication
from carbon.type.gong_authentication import GongAuthentication
from carbon.type.confluence_authentication import ConfluenceAuthentication
from carbon.type.s3_authentication import S3Authentication
from carbon.type.one_drive_authentication import OneDriveAuthentication
from carbon.type.connect_data_source_input import ConnectDataSourceInput
from carbon.type.azure_blob_storage_authentication import AzureBlobStorageAuthentication
from carbon.type.sync_options import SyncOptions

from ...api_client import Dictionary
from carbon.pydantic.connect_data_source_response import ConnectDataSourceResponse as ConnectDataSourceResponsePydantic
from carbon.pydantic.s3_authentication import S3Authentication as S3AuthenticationPydantic
from carbon.pydantic.o_auth_authentication import OAuthAuthentication as OAuthAuthenticationPydantic
from carbon.pydantic.one_drive_authentication import OneDriveAuthentication as OneDriveAuthenticationPydantic
from carbon.pydantic.http_validation_error import HTTPValidationError as HTTPValidationErrorPydantic
from carbon.pydantic.confluence_authentication import ConfluenceAuthentication as ConfluenceAuthenticationPydantic
from carbon.pydantic.salesforce_authentication import SalesforceAuthentication as SalesforceAuthenticationPydantic
from carbon.pydantic.zendesk_authentication import ZendeskAuthentication as ZendeskAuthenticationPydantic
from carbon.pydantic.azure_blob_storage_authentication import AzureBlobStorageAuthentication as AzureBlobStorageAuthenticationPydantic
from carbon.pydantic.sync_options import SyncOptions as SyncOptionsPydantic
from carbon.pydantic.sharepoint_authentication import SharepointAuthentication as SharepointAuthenticationPydantic
from carbon.pydantic.notion_authentication import NotionAuthentication as NotionAuthenticationPydantic
from carbon.pydantic.gong_authentication import GongAuthentication as GongAuthenticationPydantic
from carbon.pydantic.github_authentication import GithubAuthentication as GithubAuthenticationPydantic
from carbon.pydantic.freskdesk_authentication import FreskdeskAuthentication as FreskdeskAuthenticationPydantic
from carbon.pydantic.guru_authentication import GuruAuthentication as GuruAuthenticationPydantic
from carbon.pydantic.service_now_authentication import ServiceNowAuthentication as ServiceNowAuthenticationPydantic
from carbon.pydantic.zotero_authentication import ZoteroAuthentication as ZoteroAuthenticationPydantic
from carbon.pydantic.gitbook_authetication import GitbookAuthetication as GitbookAutheticationPydantic
from carbon.pydantic.connect_data_source_input import ConnectDataSourceInput as ConnectDataSourceInputPydantic

# body param
SchemaForRequestBodyApplicationJson = ConnectDataSourceInputSchema


request_body_connect_data_source_input = api_client.RequestBody(
    content={
        'application/json': api_client.MediaType(
            schema=SchemaForRequestBodyApplicationJson),
    },
    required=True,
)
SchemaFor200ResponseBodyApplicationJson = ConnectDataSourceResponseSchema


@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    body: ConnectDataSourceResponse


@dataclass
class ApiResponseFor200Async(api_client.AsyncApiResponse):
    body: ConnectDataSourceResponse


_response_for_200 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor200,
    response_cls_async=ApiResponseFor200Async,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor200ResponseBodyApplicationJson),
    },
)
SchemaFor422ResponseBodyApplicationJson = HTTPValidationErrorSchema


@dataclass
class ApiResponseFor422(api_client.ApiResponse):
    body: HTTPValidationError


@dataclass
class ApiResponseFor422Async(api_client.AsyncApiResponse):
    body: HTTPValidationError


_response_for_422 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor422,
    response_cls_async=ApiResponseFor422Async,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor422ResponseBodyApplicationJson),
    },
)
_all_accept_content_types = (
    'application/json',
)


class BaseApi(api_client.Api):

    def _connect_data_source_mapped_args(
        self,
        authentication: typing.Union[OAuthAuthentication, NotionAuthentication, OneDriveAuthentication, SharepointAuthentication, ConfluenceAuthentication, ZendeskAuthentication, ZoteroAuthentication, GitbookAuthetication, SalesforceAuthentication, FreskdeskAuthentication, S3Authentication, AzureBlobStorageAuthentication, GithubAuthentication, ServiceNowAuthentication, GuruAuthentication, GongAuthentication],
        sync_options: typing.Optional[SyncOptions] = None,
    ) -> api_client.MappedArgs:
        args: api_client.MappedArgs = api_client.MappedArgs()
        _body = {}
        if authentication is not None:
            _body["authentication"] = authentication
        if sync_options is not None:
            _body["sync_options"] = sync_options
        args.body = _body
        return args

    async def _aconnect_data_source_oapg(
        self,
        body: typing.Any = None,
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        content_type: str = 'application/json',
        stream: bool = False,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        """
        Connect Data Source
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        used_path = path.value
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add('Accept', accept_content_type)
        method = 'post'.upper()
        _headers.add('Content-Type', content_type)
    
        if body is schemas.unset:
            raise exceptions.ApiValueError(
                'The required body parameter has an invalid value of: unset. Set a valid value instead')
        _fields = None
        _body = None
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            path_template='/integrations/connect',
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_connect_data_source_input.serialize(body, content_type)
        if 'fields' in serialized_data:
            _fields = serialized_data['fields']
        elif 'body' in serialized_data:
            _body = serialized_data['body']
    
        response = await self.api_client.async_call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            fields=_fields,
            serialized_body=_body,
            body=body,
            auth_settings=_auth,
            timeout=timeout,
            **kwargs
        )
    
        if stream:
            if not 200 <= response.http_response.status <= 299:
                body = (await response.http_response.content.read()).decode("utf-8")
                raise exceptions.ApiStreamingException(
                    status=response.http_response.status,
                    reason=response.http_response.reason,
                    body=body,
                )
    
            async def stream_iterator():
                """
                iterates over response.http_response.content and closes connection once iteration has finished
                """
                async for line in response.http_response.content:
                    if line == b'\r\n':
                        continue
                    yield line
                response.http_response.close()
                await response.session.close()
            return AsyncGeneratorResponse(
                content=stream_iterator(),
                headers=response.http_response.headers,
                status=response.http_response.status,
                response=response.http_response
            )
    
        response_for_status = _status_code_to_response.get(str(response.http_response.status))
        if response_for_status:
            api_response = await response_for_status.deserialize_async(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
        else:
            # If response data is JSON then deserialize for SDK consumer convenience
            is_json = api_client.JSONDetector._content_type_is_json(response.http_response.headers.get('Content-Type', ''))
            api_response = api_client.ApiResponseWithoutDeserializationAsync(
                body=await response.http_response.json() if is_json else await response.http_response.text(),
                response=response.http_response,
                round_trip_time=response.round_trip_time,
                status=response.http_response.status,
                headers=response.http_response.headers,
            )
    
        if not 200 <= api_response.status <= 299:
            raise exceptions.ApiException(api_response=api_response)
    
        # cleanup session / response
        response.http_response.close()
        await response.session.close()
    
        return api_response


    def _connect_data_source_oapg(
        self,
        body: typing.Any = None,
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        content_type: str = 'application/json',
        stream: bool = False,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """
        Connect Data Source
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        used_path = path.value
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add('Accept', accept_content_type)
        method = 'post'.upper()
        _headers.add('Content-Type', content_type)
    
        if body is schemas.unset:
            raise exceptions.ApiValueError(
                'The required body parameter has an invalid value of: unset. Set a valid value instead')
        _fields = None
        _body = None
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            path_template='/integrations/connect',
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_connect_data_source_input.serialize(body, content_type)
        if 'fields' in serialized_data:
            _fields = serialized_data['fields']
        elif 'body' in serialized_data:
            _body = serialized_data['body']
    
        response = self.api_client.call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            fields=_fields,
            serialized_body=_body,
            body=body,
            auth_settings=_auth,
            timeout=timeout,
        )
    
        response_for_status = _status_code_to_response.get(str(response.http_response.status))
        if response_for_status:
            api_response = response_for_status.deserialize(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
        else:
            # If response data is JSON then deserialize for SDK consumer convenience
            is_json = api_client.JSONDetector._content_type_is_json(response.http_response.headers.get('Content-Type', ''))
            api_response = api_client.ApiResponseWithoutDeserialization(
                body=json.loads(response.http_response.data) if is_json else response.http_response.data,
                response=response.http_response,
                round_trip_time=response.round_trip_time,
                status=response.http_response.status,
                headers=response.http_response.headers,
            )
    
        if not 200 <= api_response.status <= 299:
            raise exceptions.ApiException(api_response=api_response)
    
        return api_response


class ConnectDataSourceRaw(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    async def aconnect_data_source(
        self,
        authentication: typing.Union[OAuthAuthentication, NotionAuthentication, OneDriveAuthentication, SharepointAuthentication, ConfluenceAuthentication, ZendeskAuthentication, ZoteroAuthentication, GitbookAuthetication, SalesforceAuthentication, FreskdeskAuthentication, S3Authentication, AzureBlobStorageAuthentication, GithubAuthentication, ServiceNowAuthentication, GuruAuthentication, GongAuthentication],
        sync_options: typing.Optional[SyncOptions] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._connect_data_source_mapped_args(
            authentication=authentication,
            sync_options=sync_options,
        )
        return await self._aconnect_data_source_oapg(
            body=args.body,
            **kwargs,
        )
    
    def connect_data_source(
        self,
        authentication: typing.Union[OAuthAuthentication, NotionAuthentication, OneDriveAuthentication, SharepointAuthentication, ConfluenceAuthentication, ZendeskAuthentication, ZoteroAuthentication, GitbookAuthetication, SalesforceAuthentication, FreskdeskAuthentication, S3Authentication, AzureBlobStorageAuthentication, GithubAuthentication, ServiceNowAuthentication, GuruAuthentication, GongAuthentication],
        sync_options: typing.Optional[SyncOptions] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """  """
        args = self._connect_data_source_mapped_args(
            authentication=authentication,
            sync_options=sync_options,
        )
        return self._connect_data_source_oapg(
            body=args.body,
        )

class ConnectDataSource(BaseApi):

    async def aconnect_data_source(
        self,
        authentication: typing.Union[OAuthAuthentication, NotionAuthentication, OneDriveAuthentication, SharepointAuthentication, ConfluenceAuthentication, ZendeskAuthentication, ZoteroAuthentication, GitbookAuthetication, SalesforceAuthentication, FreskdeskAuthentication, S3Authentication, AzureBlobStorageAuthentication, GithubAuthentication, ServiceNowAuthentication, GuruAuthentication, GongAuthentication],
        sync_options: typing.Optional[SyncOptions] = None,
        validate: bool = False,
        **kwargs,
    ) -> ConnectDataSourceResponsePydantic:
        raw_response = await self.raw.aconnect_data_source(
            authentication=authentication,
            sync_options=sync_options,
            **kwargs,
        )
        if validate:
            return ConnectDataSourceResponsePydantic(**raw_response.body)
        return api_client.construct_model_instance(ConnectDataSourceResponsePydantic, raw_response.body)
    
    
    def connect_data_source(
        self,
        authentication: typing.Union[OAuthAuthentication, NotionAuthentication, OneDriveAuthentication, SharepointAuthentication, ConfluenceAuthentication, ZendeskAuthentication, ZoteroAuthentication, GitbookAuthetication, SalesforceAuthentication, FreskdeskAuthentication, S3Authentication, AzureBlobStorageAuthentication, GithubAuthentication, ServiceNowAuthentication, GuruAuthentication, GongAuthentication],
        sync_options: typing.Optional[SyncOptions] = None,
        validate: bool = False,
    ) -> ConnectDataSourceResponsePydantic:
        raw_response = self.raw.connect_data_source(
            authentication=authentication,
            sync_options=sync_options,
        )
        if validate:
            return ConnectDataSourceResponsePydantic(**raw_response.body)
        return api_client.construct_model_instance(ConnectDataSourceResponsePydantic, raw_response.body)


class ApiForpost(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    async def apost(
        self,
        authentication: typing.Union[OAuthAuthentication, NotionAuthentication, OneDriveAuthentication, SharepointAuthentication, ConfluenceAuthentication, ZendeskAuthentication, ZoteroAuthentication, GitbookAuthetication, SalesforceAuthentication, FreskdeskAuthentication, S3Authentication, AzureBlobStorageAuthentication, GithubAuthentication, ServiceNowAuthentication, GuruAuthentication, GongAuthentication],
        sync_options: typing.Optional[SyncOptions] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._connect_data_source_mapped_args(
            authentication=authentication,
            sync_options=sync_options,
        )
        return await self._aconnect_data_source_oapg(
            body=args.body,
            **kwargs,
        )
    
    def post(
        self,
        authentication: typing.Union[OAuthAuthentication, NotionAuthentication, OneDriveAuthentication, SharepointAuthentication, ConfluenceAuthentication, ZendeskAuthentication, ZoteroAuthentication, GitbookAuthetication, SalesforceAuthentication, FreskdeskAuthentication, S3Authentication, AzureBlobStorageAuthentication, GithubAuthentication, ServiceNowAuthentication, GuruAuthentication, GongAuthentication],
        sync_options: typing.Optional[SyncOptions] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """  """
        args = self._connect_data_source_mapped_args(
            authentication=authentication,
            sync_options=sync_options,
        )
        return self._connect_data_source_oapg(
            body=args.body,
        )

