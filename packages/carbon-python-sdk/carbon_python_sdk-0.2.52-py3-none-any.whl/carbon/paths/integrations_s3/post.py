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

from carbon.model.http_validation_error import HTTPValidationError as HTTPValidationErrorSchema
from carbon.model.s3_auth_request import S3AuthRequest as S3AuthRequestSchema
from carbon.model.organization_user_data_source_api import OrganizationUserDataSourceAPI as OrganizationUserDataSourceAPISchema

from carbon.type.s3_auth_request import S3AuthRequest
from carbon.type.http_validation_error import HTTPValidationError
from carbon.type.organization_user_data_source_api import OrganizationUserDataSourceAPI

from ...api_client import Dictionary
from carbon.pydantic.s3_auth_request import S3AuthRequest as S3AuthRequestPydantic
from carbon.pydantic.http_validation_error import HTTPValidationError as HTTPValidationErrorPydantic
from carbon.pydantic.organization_user_data_source_api import OrganizationUserDataSourceAPI as OrganizationUserDataSourceAPIPydantic

from . import path

# body param
SchemaForRequestBodyApplicationJson = S3AuthRequestSchema


request_body_s3_auth_request = api_client.RequestBody(
    content={
        'application/json': api_client.MediaType(
            schema=SchemaForRequestBodyApplicationJson),
    },
    required=True,
)
_auth = [
    'accessToken',
    'apiKey',
    'customerId',
]
SchemaFor200ResponseBodyApplicationJson = OrganizationUserDataSourceAPISchema


@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    body: OrganizationUserDataSourceAPI


@dataclass
class ApiResponseFor200Async(api_client.AsyncApiResponse):
    body: OrganizationUserDataSourceAPI


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
_status_code_to_response = {
    '200': _response_for_200,
    '422': _response_for_422,
}
_all_accept_content_types = (
    'application/json',
)


class BaseApi(api_client.Api):

    def _create_aws_iam_user_mapped_args(
        self,
        access_key: str,
        access_key_secret: str,
        sync_source_items: typing.Optional[bool] = None,
        endpoint_url: typing.Optional[typing.Optional[str]] = None,
        data_source_tags: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
    ) -> api_client.MappedArgs:
        args: api_client.MappedArgs = api_client.MappedArgs()
        _body = {}
        if access_key is not None:
            _body["access_key"] = access_key
        if access_key_secret is not None:
            _body["access_key_secret"] = access_key_secret
        if sync_source_items is not None:
            _body["sync_source_items"] = sync_source_items
        if endpoint_url is not None:
            _body["endpoint_url"] = endpoint_url
        if data_source_tags is not None:
            _body["data_source_tags"] = data_source_tags
        args.body = _body
        return args

    async def _acreate_aws_iam_user_oapg(
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
        S3 Auth
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
            path_template='/integrations/s3',
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_s3_auth_request.serialize(body, content_type)
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


    def _create_aws_iam_user_oapg(
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
        S3 Auth
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
            path_template='/integrations/s3',
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_s3_auth_request.serialize(body, content_type)
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


class CreateAwsIamUserRaw(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    async def acreate_aws_iam_user(
        self,
        access_key: str,
        access_key_secret: str,
        sync_source_items: typing.Optional[bool] = None,
        endpoint_url: typing.Optional[typing.Optional[str]] = None,
        data_source_tags: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._create_aws_iam_user_mapped_args(
            access_key=access_key,
            access_key_secret=access_key_secret,
            sync_source_items=sync_source_items,
            endpoint_url=endpoint_url,
            data_source_tags=data_source_tags,
        )
        return await self._acreate_aws_iam_user_oapg(
            body=args.body,
            **kwargs,
        )
    
    def create_aws_iam_user(
        self,
        access_key: str,
        access_key_secret: str,
        sync_source_items: typing.Optional[bool] = None,
        endpoint_url: typing.Optional[typing.Optional[str]] = None,
        data_source_tags: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """ This endpoint can be used to connect S3 as well as Digital Ocean Spaces (S3 compatible)   For S3, create a new IAM user with permissions to: <ol> <li>List all buckets.</li> <li>Read from the specific buckets and objects to sync with Carbon. Ensure any future buckets or objects carry  the same permissions.</li> </ol> Once created, generate an access key for this user and share the credentials with us. We recommend testing this key beforehand.   For Digital Ocean Spaces, generate the above credentials in your Applications and API page here https://cloud.digitalocean.com/account/api/spaces. Endpoint URL is required to connect Digital Ocean Spaces. It should look like <<region>>.digitaloceanspaces.com """
        args = self._create_aws_iam_user_mapped_args(
            access_key=access_key,
            access_key_secret=access_key_secret,
            sync_source_items=sync_source_items,
            endpoint_url=endpoint_url,
            data_source_tags=data_source_tags,
        )
        return self._create_aws_iam_user_oapg(
            body=args.body,
        )

class CreateAwsIamUser(BaseApi):

    async def acreate_aws_iam_user(
        self,
        access_key: str,
        access_key_secret: str,
        sync_source_items: typing.Optional[bool] = None,
        endpoint_url: typing.Optional[typing.Optional[str]] = None,
        data_source_tags: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
        validate: bool = False,
        **kwargs,
    ) -> OrganizationUserDataSourceAPIPydantic:
        raw_response = await self.raw.acreate_aws_iam_user(
            access_key=access_key,
            access_key_secret=access_key_secret,
            sync_source_items=sync_source_items,
            endpoint_url=endpoint_url,
            data_source_tags=data_source_tags,
            **kwargs,
        )
        if validate:
            return OrganizationUserDataSourceAPIPydantic(**raw_response.body)
        return api_client.construct_model_instance(OrganizationUserDataSourceAPIPydantic, raw_response.body)
    
    
    def create_aws_iam_user(
        self,
        access_key: str,
        access_key_secret: str,
        sync_source_items: typing.Optional[bool] = None,
        endpoint_url: typing.Optional[typing.Optional[str]] = None,
        data_source_tags: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
        validate: bool = False,
    ) -> OrganizationUserDataSourceAPIPydantic:
        raw_response = self.raw.create_aws_iam_user(
            access_key=access_key,
            access_key_secret=access_key_secret,
            sync_source_items=sync_source_items,
            endpoint_url=endpoint_url,
            data_source_tags=data_source_tags,
        )
        if validate:
            return OrganizationUserDataSourceAPIPydantic(**raw_response.body)
        return api_client.construct_model_instance(OrganizationUserDataSourceAPIPydantic, raw_response.body)


class ApiForpost(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    async def apost(
        self,
        access_key: str,
        access_key_secret: str,
        sync_source_items: typing.Optional[bool] = None,
        endpoint_url: typing.Optional[typing.Optional[str]] = None,
        data_source_tags: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._create_aws_iam_user_mapped_args(
            access_key=access_key,
            access_key_secret=access_key_secret,
            sync_source_items=sync_source_items,
            endpoint_url=endpoint_url,
            data_source_tags=data_source_tags,
        )
        return await self._acreate_aws_iam_user_oapg(
            body=args.body,
            **kwargs,
        )
    
    def post(
        self,
        access_key: str,
        access_key_secret: str,
        sync_source_items: typing.Optional[bool] = None,
        endpoint_url: typing.Optional[typing.Optional[str]] = None,
        data_source_tags: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """ This endpoint can be used to connect S3 as well as Digital Ocean Spaces (S3 compatible)   For S3, create a new IAM user with permissions to: <ol> <li>List all buckets.</li> <li>Read from the specific buckets and objects to sync with Carbon. Ensure any future buckets or objects carry  the same permissions.</li> </ol> Once created, generate an access key for this user and share the credentials with us. We recommend testing this key beforehand.   For Digital Ocean Spaces, generate the above credentials in your Applications and API page here https://cloud.digitalocean.com/account/api/spaces. Endpoint URL is required to connect Digital Ocean Spaces. It should look like <<region>>.digitaloceanspaces.com """
        args = self._create_aws_iam_user_mapped_args(
            access_key=access_key,
            access_key_secret=access_key_secret,
            sync_source_items=sync_source_items,
            endpoint_url=endpoint_url,
            data_source_tags=data_source_tags,
        )
        return self._create_aws_iam_user_oapg(
            body=args.body,
        )

