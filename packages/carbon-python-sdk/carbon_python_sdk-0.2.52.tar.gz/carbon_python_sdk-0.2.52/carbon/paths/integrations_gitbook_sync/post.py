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

from carbon.model.gitbook_sync_request_space_ids import GitbookSyncRequestSpaceIds as GitbookSyncRequestSpaceIdsSchema
from carbon.model.http_validation_error import HTTPValidationError as HTTPValidationErrorSchema
from carbon.model.gitbook_sync_request import GitbookSyncRequest as GitbookSyncRequestSchema
from carbon.model.embedding_generators import EmbeddingGenerators as EmbeddingGeneratorsSchema
from carbon.model.file_sync_config_nullable import FileSyncConfigNullable as FileSyncConfigNullableSchema

from carbon.type.embedding_generators import EmbeddingGenerators
from carbon.type.http_validation_error import HTTPValidationError
from carbon.type.file_sync_config_nullable import FileSyncConfigNullable
from carbon.type.gitbook_sync_request_space_ids import GitbookSyncRequestSpaceIds
from carbon.type.gitbook_sync_request import GitbookSyncRequest

from ...api_client import Dictionary
from carbon.pydantic.gitbook_sync_request import GitbookSyncRequest as GitbookSyncRequestPydantic
from carbon.pydantic.http_validation_error import HTTPValidationError as HTTPValidationErrorPydantic
from carbon.pydantic.embedding_generators import EmbeddingGenerators as EmbeddingGeneratorsPydantic
from carbon.pydantic.file_sync_config_nullable import FileSyncConfigNullable as FileSyncConfigNullablePydantic
from carbon.pydantic.gitbook_sync_request_space_ids import GitbookSyncRequestSpaceIds as GitbookSyncRequestSpaceIdsPydantic

from . import path

# body param
SchemaForRequestBodyApplicationJson = GitbookSyncRequestSchema


request_body_gitbook_sync_request = api_client.RequestBody(
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
SchemaFor200ResponseBodyApplicationJson = schemas.DictSchema


@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    body: typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]


@dataclass
class ApiResponseFor200Async(api_client.AsyncApiResponse):
    body: typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]


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

    def _sync_gitbook_mapped_args(
        self,
        space_ids: GitbookSyncRequestSpaceIds,
        data_source_id: int,
        tags: typing.Optional[typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]] = None,
        chunk_size: typing.Optional[typing.Optional[int]] = None,
        chunk_overlap: typing.Optional[typing.Optional[int]] = None,
        skip_embedding_generation: typing.Optional[typing.Optional[bool]] = None,
        embedding_model: typing.Optional[EmbeddingGenerators] = None,
        generate_sparse_vectors: typing.Optional[typing.Optional[bool]] = None,
        prepend_filename_to_chunks: typing.Optional[typing.Optional[bool]] = None,
        request_id: typing.Optional[typing.Optional[str]] = None,
        file_sync_config: typing.Optional[FileSyncConfigNullable] = None,
    ) -> api_client.MappedArgs:
        args: api_client.MappedArgs = api_client.MappedArgs()
        _body = {}
        if tags is not None:
            _body["tags"] = tags
        if space_ids is not None:
            _body["space_ids"] = space_ids
        if data_source_id is not None:
            _body["data_source_id"] = data_source_id
        if chunk_size is not None:
            _body["chunk_size"] = chunk_size
        if chunk_overlap is not None:
            _body["chunk_overlap"] = chunk_overlap
        if skip_embedding_generation is not None:
            _body["skip_embedding_generation"] = skip_embedding_generation
        if embedding_model is not None:
            _body["embedding_model"] = embedding_model
        if generate_sparse_vectors is not None:
            _body["generate_sparse_vectors"] = generate_sparse_vectors
        if prepend_filename_to_chunks is not None:
            _body["prepend_filename_to_chunks"] = prepend_filename_to_chunks
        if request_id is not None:
            _body["request_id"] = request_id
        if file_sync_config is not None:
            _body["file_sync_config"] = file_sync_config
        args.body = _body
        return args

    async def _async_gitbook_oapg(
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
        Gitbook Sync
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
            path_template='/integrations/gitbook/sync',
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_gitbook_sync_request.serialize(body, content_type)
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


    def _sync_gitbook_oapg(
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
        Gitbook Sync
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
            path_template='/integrations/gitbook/sync',
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_gitbook_sync_request.serialize(body, content_type)
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


class SyncGitbookRaw(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    async def async_gitbook(
        self,
        space_ids: GitbookSyncRequestSpaceIds,
        data_source_id: int,
        tags: typing.Optional[typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]] = None,
        chunk_size: typing.Optional[typing.Optional[int]] = None,
        chunk_overlap: typing.Optional[typing.Optional[int]] = None,
        skip_embedding_generation: typing.Optional[typing.Optional[bool]] = None,
        embedding_model: typing.Optional[EmbeddingGenerators] = None,
        generate_sparse_vectors: typing.Optional[typing.Optional[bool]] = None,
        prepend_filename_to_chunks: typing.Optional[typing.Optional[bool]] = None,
        request_id: typing.Optional[typing.Optional[str]] = None,
        file_sync_config: typing.Optional[FileSyncConfigNullable] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._sync_gitbook_mapped_args(
            space_ids=space_ids,
            data_source_id=data_source_id,
            tags=tags,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            skip_embedding_generation=skip_embedding_generation,
            embedding_model=embedding_model,
            generate_sparse_vectors=generate_sparse_vectors,
            prepend_filename_to_chunks=prepend_filename_to_chunks,
            request_id=request_id,
            file_sync_config=file_sync_config,
        )
        return await self._async_gitbook_oapg(
            body=args.body,
            **kwargs,
        )
    
    def sync_gitbook(
        self,
        space_ids: GitbookSyncRequestSpaceIds,
        data_source_id: int,
        tags: typing.Optional[typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]] = None,
        chunk_size: typing.Optional[typing.Optional[int]] = None,
        chunk_overlap: typing.Optional[typing.Optional[int]] = None,
        skip_embedding_generation: typing.Optional[typing.Optional[bool]] = None,
        embedding_model: typing.Optional[EmbeddingGenerators] = None,
        generate_sparse_vectors: typing.Optional[typing.Optional[bool]] = None,
        prepend_filename_to_chunks: typing.Optional[typing.Optional[bool]] = None,
        request_id: typing.Optional[typing.Optional[str]] = None,
        file_sync_config: typing.Optional[FileSyncConfigNullable] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """ You can sync upto 20 Gitbook spaces at a time using this endpoint. Additional parameters below can be used to associate  data with the synced pages or modify the sync behavior. """
        args = self._sync_gitbook_mapped_args(
            space_ids=space_ids,
            data_source_id=data_source_id,
            tags=tags,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            skip_embedding_generation=skip_embedding_generation,
            embedding_model=embedding_model,
            generate_sparse_vectors=generate_sparse_vectors,
            prepend_filename_to_chunks=prepend_filename_to_chunks,
            request_id=request_id,
            file_sync_config=file_sync_config,
        )
        return self._sync_gitbook_oapg(
            body=args.body,
        )

class SyncGitbook(BaseApi):

    async def async_gitbook(
        self,
        space_ids: GitbookSyncRequestSpaceIds,
        data_source_id: int,
        tags: typing.Optional[typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]] = None,
        chunk_size: typing.Optional[typing.Optional[int]] = None,
        chunk_overlap: typing.Optional[typing.Optional[int]] = None,
        skip_embedding_generation: typing.Optional[typing.Optional[bool]] = None,
        embedding_model: typing.Optional[EmbeddingGenerators] = None,
        generate_sparse_vectors: typing.Optional[typing.Optional[bool]] = None,
        prepend_filename_to_chunks: typing.Optional[typing.Optional[bool]] = None,
        request_id: typing.Optional[typing.Optional[str]] = None,
        file_sync_config: typing.Optional[FileSyncConfigNullable] = None,
        validate: bool = False,
        **kwargs,
    ) -> Dictionary:
        raw_response = await self.raw.async_gitbook(
            space_ids=space_ids,
            data_source_id=data_source_id,
            tags=tags,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            skip_embedding_generation=skip_embedding_generation,
            embedding_model=embedding_model,
            generate_sparse_vectors=generate_sparse_vectors,
            prepend_filename_to_chunks=prepend_filename_to_chunks,
            request_id=request_id,
            file_sync_config=file_sync_config,
            **kwargs,
        )
        if validate:
            return Dictionary(**raw_response.body)
        return api_client.construct_model_instance(Dictionary, raw_response.body)
    
    
    def sync_gitbook(
        self,
        space_ids: GitbookSyncRequestSpaceIds,
        data_source_id: int,
        tags: typing.Optional[typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]] = None,
        chunk_size: typing.Optional[typing.Optional[int]] = None,
        chunk_overlap: typing.Optional[typing.Optional[int]] = None,
        skip_embedding_generation: typing.Optional[typing.Optional[bool]] = None,
        embedding_model: typing.Optional[EmbeddingGenerators] = None,
        generate_sparse_vectors: typing.Optional[typing.Optional[bool]] = None,
        prepend_filename_to_chunks: typing.Optional[typing.Optional[bool]] = None,
        request_id: typing.Optional[typing.Optional[str]] = None,
        file_sync_config: typing.Optional[FileSyncConfigNullable] = None,
        validate: bool = False,
    ) -> Dictionary:
        raw_response = self.raw.sync_gitbook(
            space_ids=space_ids,
            data_source_id=data_source_id,
            tags=tags,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            skip_embedding_generation=skip_embedding_generation,
            embedding_model=embedding_model,
            generate_sparse_vectors=generate_sparse_vectors,
            prepend_filename_to_chunks=prepend_filename_to_chunks,
            request_id=request_id,
            file_sync_config=file_sync_config,
        )
        if validate:
            return Dictionary(**raw_response.body)
        return api_client.construct_model_instance(Dictionary, raw_response.body)


class ApiForpost(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    async def apost(
        self,
        space_ids: GitbookSyncRequestSpaceIds,
        data_source_id: int,
        tags: typing.Optional[typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]] = None,
        chunk_size: typing.Optional[typing.Optional[int]] = None,
        chunk_overlap: typing.Optional[typing.Optional[int]] = None,
        skip_embedding_generation: typing.Optional[typing.Optional[bool]] = None,
        embedding_model: typing.Optional[EmbeddingGenerators] = None,
        generate_sparse_vectors: typing.Optional[typing.Optional[bool]] = None,
        prepend_filename_to_chunks: typing.Optional[typing.Optional[bool]] = None,
        request_id: typing.Optional[typing.Optional[str]] = None,
        file_sync_config: typing.Optional[FileSyncConfigNullable] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._sync_gitbook_mapped_args(
            space_ids=space_ids,
            data_source_id=data_source_id,
            tags=tags,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            skip_embedding_generation=skip_embedding_generation,
            embedding_model=embedding_model,
            generate_sparse_vectors=generate_sparse_vectors,
            prepend_filename_to_chunks=prepend_filename_to_chunks,
            request_id=request_id,
            file_sync_config=file_sync_config,
        )
        return await self._async_gitbook_oapg(
            body=args.body,
            **kwargs,
        )
    
    def post(
        self,
        space_ids: GitbookSyncRequestSpaceIds,
        data_source_id: int,
        tags: typing.Optional[typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]] = None,
        chunk_size: typing.Optional[typing.Optional[int]] = None,
        chunk_overlap: typing.Optional[typing.Optional[int]] = None,
        skip_embedding_generation: typing.Optional[typing.Optional[bool]] = None,
        embedding_model: typing.Optional[EmbeddingGenerators] = None,
        generate_sparse_vectors: typing.Optional[typing.Optional[bool]] = None,
        prepend_filename_to_chunks: typing.Optional[typing.Optional[bool]] = None,
        request_id: typing.Optional[typing.Optional[str]] = None,
        file_sync_config: typing.Optional[FileSyncConfigNullable] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """ You can sync upto 20 Gitbook spaces at a time using this endpoint. Additional parameters below can be used to associate  data with the synced pages or modify the sync behavior. """
        args = self._sync_gitbook_mapped_args(
            space_ids=space_ids,
            data_source_id=data_source_id,
            tags=tags,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            skip_embedding_generation=skip_embedding_generation,
            embedding_model=embedding_model,
            generate_sparse_vectors=generate_sparse_vectors,
            prepend_filename_to_chunks=prepend_filename_to_chunks,
            request_id=request_id,
            file_sync_config=file_sync_config,
        )
        return self._sync_gitbook_oapg(
            body=args.body,
        )

