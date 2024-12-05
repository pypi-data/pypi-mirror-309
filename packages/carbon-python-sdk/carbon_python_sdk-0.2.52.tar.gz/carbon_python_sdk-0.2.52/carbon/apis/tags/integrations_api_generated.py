# coding: utf-8
"""
    Carbon

    Connect external data to LLMs, no matter the source.

    The version of the OpenAPI document: 1.0.0
    Generated by: https://konfigthis.com
"""

from carbon.paths.integrations_items_sync_cancel.post import Cancel
from carbon.paths.integrations_connect.post import ConnectDataSource
from carbon.paths.integrations_freshdesk.post import ConnectFreshdesk
from carbon.paths.integrations_gitbook.post import ConnectGitbook
from carbon.paths.integrations_guru.post import ConnectGuru
from carbon.paths.integrations_s3.post import CreateAwsIamUser
from carbon.paths.integrations_oauth_url.post import GetOauthUrl
from carbon.paths.integrations_confluence_list.post import ListConfluencePages
from carbon.paths.integrations_slack_conversations.get import ListConversations
from carbon.paths.integrations_items_list.post import ListDataSourceItems
from carbon.paths.integrations_outlook_user_folders.get import ListFolders
from carbon.paths.integrations_gitbook_spaces.get import ListGitbookSpaces
from carbon.paths.integrations_gmail_user_labels.get import ListLabels
from carbon.paths.integrations_outlook_user_categories.get import ListOutlookCategories
from carbon.paths.integrations_github_repos.get import ListRepos
from carbon.paths.integrations_sharepoint_sites_list.get import ListSharepointSites
from carbon.paths.integrations_azure_blob_storage_files.post import SyncAzureBlobFiles
from carbon.paths.integrations_azure_blob_storage.post import SyncAzureBlobStorage
from carbon.paths.integrations_confluence_sync.post import SyncConfluence
from carbon.paths.integrations_items_sync.post import SyncDataSourceItems
from carbon.paths.integrations_files_sync.post import SyncFiles
from carbon.paths.integrations_github.post import SyncGitHub
from carbon.paths.integrations_gitbook_sync.post import SyncGitbook
from carbon.paths.integrations_gmail_sync.post import SyncGmail
from carbon.paths.integrations_outlook_sync.post import SyncOutlook
from carbon.paths.integrations_github_sync_repos.post import SyncRepos
from carbon.paths.integrations_rss_feed.post import SyncRssFeed
from carbon.paths.integrations_s3_files.post import SyncS3Files
from carbon.paths.integrations_slack_sync.post import SyncSlack
from carbon.apis.tags.integrations_api_raw import IntegrationsApiRaw


class IntegrationsApiGenerated(
    Cancel,
    ConnectDataSource,
    ConnectFreshdesk,
    ConnectGitbook,
    ConnectGuru,
    CreateAwsIamUser,
    GetOauthUrl,
    ListConfluencePages,
    ListConversations,
    ListDataSourceItems,
    ListFolders,
    ListGitbookSpaces,
    ListLabels,
    ListOutlookCategories,
    ListRepos,
    ListSharepointSites,
    SyncAzureBlobFiles,
    SyncAzureBlobStorage,
    SyncConfluence,
    SyncDataSourceItems,
    SyncFiles,
    SyncGitHub,
    SyncGitbook,
    SyncGmail,
    SyncOutlook,
    SyncRepos,
    SyncRssFeed,
    SyncS3Files,
    SyncSlack,
):
    """NOTE:
    This class is auto generated by Konfig (https://konfigthis.com)
    """
    raw: IntegrationsApiRaw

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.raw = IntegrationsApiRaw(api_client)
