from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.main.apiclient import BaseApiClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.util.exceptions import InsufficientConfigArgumentsException
from splitapiclient.microclients import TrafficTypeMicroClient
from splitapiclient.microclients import EnvironmentMicroClient
from splitapiclient.microclients import SplitMicroClient
from splitapiclient.microclients import SplitDefinitionMicroClient
from splitapiclient.microclients import SegmentMicroClient
from splitapiclient.microclients import SegmentDefinitionMicroClient
from splitapiclient.microclients import WorkspaceMicroClient
from splitapiclient.microclients import IdentityMicroClient
from splitapiclient.microclients import AttributeMicroClient
from splitapiclient.microclients import ChangeRequestMicroClient
from splitapiclient.microclients import UserMicroClient
from splitapiclient.microclients import GroupMicroClient
from splitapiclient.microclients import APIKeyMicroClient
from splitapiclient.microclients import RestrictionMicroClient


class SyncApiClient(BaseApiClient):
    '''
    Synchronous Split API client
    '''

    BASE_PROD_URL = 'https://api.split.io/internal/api/v2'
    BASE_PROD_URL_OLD = 'https://api.split.io/internal/api/v1'

    def __init__(self, config):
        '''
        Class constructor.

        :param config: Dictionary containing optiones required to instantiate
            the API client. Shoud have AT LEAST the following keys:
                - 'base_url': Base url where the API is hosted
                - 'apikey': APIKey used to authenticate the user.
        '''
        if 'base_url' in config:
            self._base_url = config['base_url']
        else:
            self._base_url = self.BASE_PROD_URL
            self._base_url_old = self.BASE_PROD_URL_OLD

        missing = [i for i in ['apikey'] if i not in config]
        if missing:
            raise InsufficientConfigArgumentsException(
                'The following keys must be present in the config dict: %s'
                % ','.join(missing)
            )

        self._apikey = config['apikey']
        
        http_client = SyncHttpClient(self._base_url, self._apikey)
        self._environment_client = EnvironmentMicroClient(http_client)
        self._split_client = SplitMicroClient(http_client)
        self._split_definition_client = SplitDefinitionMicroClient(http_client)
        self._segment_client = SegmentMicroClient(http_client)
        self._segment_definition_client = SegmentDefinitionMicroClient(http_client)
        self._workspace_client = WorkspaceMicroClient(http_client)
        self._traffic_type_client = TrafficTypeMicroClient(http_client)
        self._attribute_client = AttributeMicroClient(http_client)
        self._identity_client = IdentityMicroClient(http_client)
        self._change_request_client = ChangeRequestMicroClient(http_client)
        self._user_client = UserMicroClient(http_client)
        self._group_client = GroupMicroClient(http_client)
        self._apikey_client = APIKeyMicroClient(http_client)
        self._restriction_client = RestrictionMicroClient(http_client)

    @property
    def traffic_types(self):
        return self._traffic_type_client

    @property
    def environments(self):
        return self._environment_client

    @property
    def splits(self):
        return self._split_client

    @property
    def split_definitions(self):
        return self._split_definition_client

    @property
    def segments(self):
        return self._segment_client

    @property
    def segment_definitions(self):
        return self._segment_definition_client

    @property
    def workspaces(self):
        return self._workspace_client

    @property
    def attributes(self):
        return self._attribute_client

    @property
    def identities(self):
        return self._identity_client

    @property
    def change_requests(self):
        return self._change_request_client

    @property
    def users(self):
        return self._user_client

    @property
    def groups(self):
        return self._group_client

    @property
    def apikeys(self):
        return self._apikey_client

    @property
    def restrictions(self):
        return self._restriction_client
