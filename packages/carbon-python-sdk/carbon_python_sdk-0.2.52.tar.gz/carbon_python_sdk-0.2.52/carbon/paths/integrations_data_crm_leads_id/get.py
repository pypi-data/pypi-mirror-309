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

from carbon.model.base_includes import BaseIncludes as BaseIncludesSchema
from carbon.model.http_validation_error import HTTPValidationError as HTTPValidationErrorSchema
from carbon.model.lead import Lead as LeadSchema

from carbon.type.http_validation_error import HTTPValidationError
from carbon.type.base_includes import BaseIncludes
from carbon.type.lead import Lead

from ...api_client import Dictionary
from carbon.pydantic.base_includes import BaseIncludes as BaseIncludesPydantic
from carbon.pydantic.http_validation_error import HTTPValidationError as HTTPValidationErrorPydantic
from carbon.pydantic.lead import Lead as LeadPydantic

from . import path

# Query params
DataSourceIdSchema = schemas.IntSchema
IncludeRemoteDataSchema = schemas.BoolSchema


class IncludesSchema(
    schemas.ListSchema
):


    class MetaOapg:
        
        @staticmethod
        def items() -> typing.Type['BaseIncludes']:
            return BaseIncludes

    def __new__(
        cls,
        arg: typing.Union[typing.Tuple['BaseIncludes'], typing.List['BaseIncludes']],
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'IncludesSchema':
        return super().__new__(
            cls,
            arg,
            _configuration=_configuration,
        )

    def __getitem__(self, i: int) -> 'BaseIncludes':
        return super().__getitem__(i)
RequestRequiredQueryParams = typing_extensions.TypedDict(
    'RequestRequiredQueryParams',
    {
        'data_source_id': typing.Union[DataSourceIdSchema, decimal.Decimal, int, ],
    }
)
RequestOptionalQueryParams = typing_extensions.TypedDict(
    'RequestOptionalQueryParams',
    {
        'include_remote_data': typing.Union[IncludeRemoteDataSchema, bool, ],
        'includes': typing.Union[IncludesSchema, list, tuple, ],
    },
    total=False
)


class RequestQueryParams(RequestRequiredQueryParams, RequestOptionalQueryParams):
    pass


request_query_data_source_id = api_client.QueryParameter(
    name="data_source_id",
    style=api_client.ParameterStyle.FORM,
    schema=DataSourceIdSchema,
    required=True,
    explode=True,
)
request_query_include_remote_data = api_client.QueryParameter(
    name="include_remote_data",
    style=api_client.ParameterStyle.FORM,
    schema=IncludeRemoteDataSchema,
    explode=True,
)
request_query_includes = api_client.QueryParameter(
    name="includes",
    style=api_client.ParameterStyle.FORM,
    schema=IncludesSchema,
    explode=True,
)
# Path params
IdSchema = schemas.StrSchema
RequestRequiredPathParams = typing_extensions.TypedDict(
    'RequestRequiredPathParams',
    {
        'id': typing.Union[IdSchema, str, ],
    }
)
RequestOptionalPathParams = typing_extensions.TypedDict(
    'RequestOptionalPathParams',
    {
    },
    total=False
)


class RequestPathParams(RequestRequiredPathParams, RequestOptionalPathParams):
    pass


request_path_id = api_client.PathParameter(
    name="id",
    style=api_client.ParameterStyle.SIMPLE,
    schema=IdSchema,
    required=True,
)
_auth = [
    'accessToken',
    'apiKey',
    'customerId',
]
SchemaFor200ResponseBodyApplicationJson = LeadSchema


@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    body: Lead


@dataclass
class ApiResponseFor200Async(api_client.AsyncApiResponse):
    body: Lead


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

    def _get_lead_mapped_args(
        self,
        id: str,
        data_source_id: int,
        include_remote_data: typing.Optional[bool] = None,
        includes: typing.Optional[typing.List[BaseIncludes]] = None,
    ) -> api_client.MappedArgs:
        args: api_client.MappedArgs = api_client.MappedArgs()
        _query_params = {}
        _path_params = {}
        if data_source_id is not None:
            _query_params["data_source_id"] = data_source_id
        if include_remote_data is not None:
            _query_params["include_remote_data"] = include_remote_data
        if includes is not None:
            _query_params["includes"] = includes
        if id is not None:
            _path_params["id"] = id
        args.query = _query_params
        args.path = _path_params
        return args

    async def _aget_lead_oapg(
        self,
            query_params: typing.Optional[dict] = {},
            path_params: typing.Optional[dict] = {},
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        """
        Get Lead
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        self._verify_typed_dict_inputs_oapg(RequestQueryParams, query_params)
        self._verify_typed_dict_inputs_oapg(RequestPathParams, path_params)
        used_path = path.value
    
        _path_params = {}
        for parameter in (
            request_path_id,
        ):
            parameter_data = path_params.get(parameter.name, schemas.unset)
            if parameter_data is schemas.unset:
                continue
            serialized_data = parameter.serialize(parameter_data)
            _path_params.update(serialized_data)
    
        for k, v in _path_params.items():
            used_path = used_path.replace('{%s}' % k, v)
    
        prefix_separator_iterator = None
        for parameter in (
            request_query_data_source_id,
            request_query_include_remote_data,
            request_query_includes,
        ):
            parameter_data = query_params.get(parameter.name, schemas.unset)
            if parameter_data is schemas.unset:
                continue
            if prefix_separator_iterator is None:
                prefix_separator_iterator = parameter.get_prefix_separator_iterator()
            serialized_data = parameter.serialize(parameter_data, prefix_separator_iterator)
            for serialized_value in serialized_data.values():
                used_path += serialized_value
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add('Accept', accept_content_type)
        method = 'get'.upper()
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            path_template='/integrations/data/crm/leads/{id}',
            auth_settings=_auth,
            headers=_headers,
        )
    
        response = await self.api_client.async_call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            auth_settings=_auth,
            prefix_separator_iterator=prefix_separator_iterator,
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


    def _get_lead_oapg(
        self,
            query_params: typing.Optional[dict] = {},
            path_params: typing.Optional[dict] = {},
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """
        Get Lead
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        self._verify_typed_dict_inputs_oapg(RequestQueryParams, query_params)
        self._verify_typed_dict_inputs_oapg(RequestPathParams, path_params)
        used_path = path.value
    
        _path_params = {}
        for parameter in (
            request_path_id,
        ):
            parameter_data = path_params.get(parameter.name, schemas.unset)
            if parameter_data is schemas.unset:
                continue
            serialized_data = parameter.serialize(parameter_data)
            _path_params.update(serialized_data)
    
        for k, v in _path_params.items():
            used_path = used_path.replace('{%s}' % k, v)
    
        prefix_separator_iterator = None
        for parameter in (
            request_query_data_source_id,
            request_query_include_remote_data,
            request_query_includes,
        ):
            parameter_data = query_params.get(parameter.name, schemas.unset)
            if parameter_data is schemas.unset:
                continue
            if prefix_separator_iterator is None:
                prefix_separator_iterator = parameter.get_prefix_separator_iterator()
            serialized_data = parameter.serialize(parameter_data, prefix_separator_iterator)
            for serialized_value in serialized_data.values():
                used_path += serialized_value
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add('Accept', accept_content_type)
        method = 'get'.upper()
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            path_template='/integrations/data/crm/leads/{id}',
            auth_settings=_auth,
            headers=_headers,
        )
    
        response = self.api_client.call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            auth_settings=_auth,
            prefix_separator_iterator=prefix_separator_iterator,
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


class GetLeadRaw(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    async def aget_lead(
        self,
        id: str,
        data_source_id: int,
        include_remote_data: typing.Optional[bool] = None,
        includes: typing.Optional[typing.List[BaseIncludes]] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._get_lead_mapped_args(
            id=id,
            data_source_id=data_source_id,
            include_remote_data=include_remote_data,
            includes=includes,
        )
        return await self._aget_lead_oapg(
            query_params=args.query,
            path_params=args.path,
            **kwargs,
        )
    
    def get_lead(
        self,
        id: str,
        data_source_id: int,
        include_remote_data: typing.Optional[bool] = None,
        includes: typing.Optional[typing.List[BaseIncludes]] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """  """
        args = self._get_lead_mapped_args(
            id=id,
            data_source_id=data_source_id,
            include_remote_data=include_remote_data,
            includes=includes,
        )
        return self._get_lead_oapg(
            query_params=args.query,
            path_params=args.path,
        )

class GetLead(BaseApi):

    async def aget_lead(
        self,
        id: str,
        data_source_id: int,
        include_remote_data: typing.Optional[bool] = None,
        includes: typing.Optional[typing.List[BaseIncludes]] = None,
        validate: bool = False,
        **kwargs,
    ) -> LeadPydantic:
        raw_response = await self.raw.aget_lead(
            id=id,
            data_source_id=data_source_id,
            include_remote_data=include_remote_data,
            includes=includes,
            **kwargs,
        )
        if validate:
            return LeadPydantic(**raw_response.body)
        return api_client.construct_model_instance(LeadPydantic, raw_response.body)
    
    
    def get_lead(
        self,
        id: str,
        data_source_id: int,
        include_remote_data: typing.Optional[bool] = None,
        includes: typing.Optional[typing.List[BaseIncludes]] = None,
        validate: bool = False,
    ) -> LeadPydantic:
        raw_response = self.raw.get_lead(
            id=id,
            data_source_id=data_source_id,
            include_remote_data=include_remote_data,
            includes=includes,
        )
        if validate:
            return LeadPydantic(**raw_response.body)
        return api_client.construct_model_instance(LeadPydantic, raw_response.body)


class ApiForget(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    async def aget(
        self,
        id: str,
        data_source_id: int,
        include_remote_data: typing.Optional[bool] = None,
        includes: typing.Optional[typing.List[BaseIncludes]] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._get_lead_mapped_args(
            id=id,
            data_source_id=data_source_id,
            include_remote_data=include_remote_data,
            includes=includes,
        )
        return await self._aget_lead_oapg(
            query_params=args.query,
            path_params=args.path,
            **kwargs,
        )
    
    def get(
        self,
        id: str,
        data_source_id: int,
        include_remote_data: typing.Optional[bool] = None,
        includes: typing.Optional[typing.List[BaseIncludes]] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """  """
        args = self._get_lead_mapped_args(
            id=id,
            data_source_id=data_source_id,
            include_remote_data=include_remote_data,
            includes=includes,
        )
        return self._get_lead_oapg(
            query_params=args.query,
            path_params=args.path,
        )

