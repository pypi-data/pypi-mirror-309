# coding: utf-8
"""
    Carbon

    Connect external data to LLMs, no matter the source.

    The version of the OpenAPI document: 1.0.0
    Generated by: https://konfigthis.com
"""

from carbon.paths.data_sources_tags_add.post import AddTags
from carbon.paths.data_sources.post import Query
from carbon.paths.user_data_sources.post import QueryUserDataSources
from carbon.paths.data_sources_tags_remove.post import RemoveTags
from carbon.paths.revoke_access_token.post import RevokeAccessToken
from carbon.apis.tags.data_sources_api_raw import DataSourcesApiRaw


class DataSourcesApiGenerated(
    AddTags,
    Query,
    QueryUserDataSources,
    RemoveTags,
    RevokeAccessToken,
):
    """NOTE:
    This class is auto generated by Konfig (https://konfigthis.com)
    """
    raw: DataSourcesApiRaw

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.raw = DataSourcesApiRaw(api_client)
