# coding: utf-8

"""
    Carbon

    Connect external data to LLMs, no matter the source.

    The version of the OpenAPI document: 1.0.0
    Generated by: https://konfigthis.com
"""

from datetime import datetime, date
import typing
from enum import Enum
from typing_extensions import TypedDict, Literal, TYPE_CHECKING

from carbon.type.file_sync_config_auto_synced_source_types import FileSyncConfigAutoSyncedSourceTypes
from carbon.type.transcription_service_nullable import TranscriptionServiceNullable

class RequiredFileSyncConfig(TypedDict):
    pass

class OptionalFileSyncConfig(TypedDict, total=False):
    auto_synced_source_types: FileSyncConfigAutoSyncedSourceTypes

    # Automatically sync attachments from files where supported. Currently applies to Helpdesk Tickets
    sync_attachments: bool

    # Detect audio language before transcription for audio files
    detect_audio_language: bool

    transcription_service: typing.Optional[TranscriptionServiceNullable]

    # Detect multiple speakers and label segments of speech by speaker for audio files.
    include_speaker_labels: bool

    # Whether to split tabular rows into chunks. Currently only valid for CSV, TSV, and XLSX files.
    split_rows: bool

    # If this flag is enabled, the file will be chunked and stored with Carbon,           but no embeddings will be generated. This overrides the skip_embedding_generation flag.
    generate_chunks_only: bool

    # If this flag is enabled, the file will be stored with Carbon, but no chunks or embeddings will be generated.            This overrides the skip_embedding_generation and generate_chunks_only flags.
    store_file_only: bool

    # Setting this flag will create a new file record with Carbon but skip any and all processing.          This means that we do not download the remote file content or generate any chunks or embeddings. We will store         some metadata like name, external id, and external URL depending on the source you are syncing from. Note that this          flag overrides both skip_embedding_generation and generate_chunks_only flags. The file will be moved to          READY_TO_SYNC status.
    skip_file_processing: bool

class FileSyncConfig(RequiredFileSyncConfig, OptionalFileSyncConfig):
    pass
