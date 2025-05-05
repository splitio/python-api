from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.main.apiclient import BaseApiClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
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
from splitapiclient.microclients import APIKeyMicroClient
from splitapiclient.microclients import FlagSetMicroClient
from splitapiclient.microclients import LargeSegmentMicroClient
from splitapiclient.microclients import LargeSegmentDefinitionMicroClient
from splitapiclient.microclients.harness import TokenMicroClient
from splitapiclient.microclients.harness import HarnessApiKeyMicroClient
from splitapiclient.microclients.harness import ServiceAccountMicroClient
from splitapiclient.microclients.harness import HarnessUserMicroClient
from splitapiclient.microclients.harness import HarnessGroupMicroClient
from splitapiclient.microclients.harness import RoleMicroClient
from splitapiclient.microclients.harness import ResourceGroupMicroClient
from splitapiclient.microclients.harness import RoleAssignmentMicroClient
from splitapiclient.microclients.harness import HarnessProjectMicroClient


class HarnessApiClient(BaseApiClient):
    '''
    Harness mode Split API client
    '''
    # Split base URLs for existing endpoints
    BASE_PROD_URL_V3 = 'https://api.split.io/api/v3'
    BASE_PROD_URL = 'https://api.split.io/internal/api/v2'
    BASE_PROD_URL_OLD = 'https://api.split.io/internal/api/v1'
    
    # Harness base URL for Harness-specific endpoints
    BASE_HARNESS_URL = 'https://app.harness.io/'

    def __init__(self, config):
        '''
        Class constructor.

        :param config: Dictionary containing options required to instantiate
            the API client. Should have AT LEAST one of the following keys:
                - 'apikey': Split API key for authentication with Split endpoints
                - 'harness_token': Harness authentication token used for x-api-key header with Harness endpoints
                  If harness_token is not provided, apikey will be used for all operations
                - 'base_url': Base url where the Split API is hosted (optional, defaults to Split URL)
                - 'base_url_v3': Base url where the Split API v3 is hosted (optional, defaults to Split URL)
                - 'harness_base_url': Base url where the Harness API is hosted (optional, defaults to Harness URL)
                - 'account_identifier': Harness account identifier to use for all Harness operations (optional)
        '''
        # Set up Split API base URLs for existing endpoints
        if 'base_url' in config:
            self._base_url = config['base_url']
        else:
            self._base_url = self.BASE_PROD_URL
            self._base_url_old = self.BASE_PROD_URL_OLD
            
        if 'base_url_v3' in config:
            self._base_url_v3 = config['base_url_v3']
        else:
            self._base_url_v3 = self.BASE_PROD_URL_V3
            
        # Set up Harness API base URL for Harness-specific endpoints
        if 'harness_base_url' in config:
            self._harness_base_url = config['harness_base_url']
        else:
            self._harness_base_url = self.BASE_HARNESS_URL

        # Check if at least one authentication method is provided
        if 'apikey' not in config and 'harness_token' not in config:
            raise InsufficientConfigArgumentsException(
                'At least one of the following keys must be present in the config dict for harness mode: apikey, harness_token'
            )

        # Set up authentication tokens
        self._apikey = config.get('apikey')
        self._harness_token = config.get('harness_token')
        
        # If harness_token is not provided, use apikey for all operations
        # If apikey is not provided, use harness_token for all operations
        split_auth_token = self._apikey if self._apikey else self._harness_token
        harness_auth_token = self._harness_token if self._harness_token else self._apikey
        
        # Store the account identifier
        self._account_identifier = config.get('account_identifier')
        
        # Create HTTP clients for Split endpoints
        split_http_client = HarnessHttpClient(self._base_url, split_auth_token)
        split_http_clientv3 = HarnessHttpClient(self._base_url_v3, split_auth_token)
        
        # Create HTTP client for Harness endpoints
        harness_http_client = HarnessHttpClient(self._harness_base_url, harness_auth_token)
        
        # Standard microclients using Split endpoints
        self._environment_client = EnvironmentMicroClient(split_http_client)
        self._split_client = SplitMicroClient(split_http_client)
        self._split_definition_client = SplitDefinitionMicroClient(split_http_client)
        self._segment_client = SegmentMicroClient(split_http_client)
        self._segment_definition_client = SegmentDefinitionMicroClient(split_http_client)
        self._large_segment_client = LargeSegmentMicroClient(split_http_client)
        self._large_segment_definition_client = LargeSegmentDefinitionMicroClient(split_http_client)
        self._workspace_client = WorkspaceMicroClient(split_http_client)
        self._traffic_type_client = TrafficTypeMicroClient(split_http_client)
        self._attribute_client = AttributeMicroClient(split_http_client)
        self._identity_client = IdentityMicroClient(split_http_client)
        self._change_request_client = ChangeRequestMicroClient(split_http_client)
        self._apikey_client = APIKeyMicroClient(split_http_client)
        self._flag_set_client = FlagSetMicroClient(split_http_clientv3)
        
        # Harness-specific microclients using Harness endpoints
        self._token_client = TokenMicroClient(harness_http_client, self._account_identifier)
        self._harness_apikey_client = HarnessApiKeyMicroClient(harness_http_client, self._account_identifier)
        self._service_account_client = ServiceAccountMicroClient(harness_http_client, self._account_identifier)
        self._harness_user_client = HarnessUserMicroClient(harness_http_client, self._account_identifier)
        self._harness_group_client = HarnessGroupMicroClient(harness_http_client, self._account_identifier)
        self._role_client = RoleMicroClient(harness_http_client, self._account_identifier)
        self._resource_group_client = ResourceGroupMicroClient(harness_http_client, self._account_identifier)
        self._role_assignment_client = RoleAssignmentMicroClient(harness_http_client, self._account_identifier)
        self._harness_project_client = HarnessProjectMicroClient(harness_http_client, self._account_identifier)

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
    def large_segments(self):
        return self._large_segment_client

    @property
    def large_segment_definitions(self):
        return self._large_segment_definition_client

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
    def apikeys(self):
        return self._apikey_client
    
    @property
    def flag_sets(self):
        return self._flag_set_client
        
    # Harness-specific properties
    
    @property
    def token(self):
        return self._token_client
        
    @property
    def harness_apikey(self):
        return self._harness_apikey_client
        
    @property
    def service_account(self):
        return self._service_account_client
        
    @property
    def harness_user(self):
        return self._harness_user_client
        
    @property
    def harness_group(self):
        return self._harness_group_client
        
    @property
    def role(self):
        return self._role_client
        
    @property
    def resource_group(self):
        return self._resource_group_client
        
    @property
    def role_assignment(self):
        return self._role_assignment_client
        
    @property
    def harness_project(self):
        return self._harness_project_client
