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

from carbon.type.azure_blob_storage_authentication import AzureBlobStorageAuthentication
from carbon.type.confluence_authentication import ConfluenceAuthentication
from carbon.type.freskdesk_authentication import FreskdeskAuthentication
from carbon.type.gitbook_authetication import GitbookAuthetication
from carbon.type.github_authentication import GithubAuthentication
from carbon.type.gong_authentication import GongAuthentication
from carbon.type.guru_authentication import GuruAuthentication
from carbon.type.notion_authentication import NotionAuthentication
from carbon.type.o_auth_authentication import OAuthAuthentication
from carbon.type.one_drive_authentication import OneDriveAuthentication
from carbon.type.s3_authentication import S3Authentication
from carbon.type.salesforce_authentication import SalesforceAuthentication
from carbon.type.service_now_authentication import ServiceNowAuthentication
from carbon.type.sharepoint_authentication import SharepointAuthentication
from carbon.type.sync_options import SyncOptions
from carbon.type.zendesk_authentication import ZendeskAuthentication
from carbon.type.zotero_authentication import ZoteroAuthentication

class RequiredConnectDataSourceInput(TypedDict):
    authentication: typing.Union[OAuthAuthentication, NotionAuthentication, OneDriveAuthentication, SharepointAuthentication, ConfluenceAuthentication, ZendeskAuthentication, ZoteroAuthentication, GitbookAuthetication, SalesforceAuthentication, FreskdeskAuthentication, S3Authentication, AzureBlobStorageAuthentication, GithubAuthentication, ServiceNowAuthentication, GuruAuthentication, GongAuthentication]


class OptionalConnectDataSourceInput(TypedDict, total=False):
    sync_options: SyncOptions

class ConnectDataSourceInput(RequiredConnectDataSourceInput, OptionalConnectDataSourceInput):
    pass
