from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.main.harness_apiclient import HarnessApiClient
from splitapiclient.util.exceptions import HarnessDeprecatedEndpointError


class TestHarnessApiClientRestrictions:
    '''
    Tests to verify that HarnessApiClient properly enforces endpoint restrictions in Harness mode
    '''
    
    def test_workspaces_restrictions(self, mocker):
        '''
        Test that workspace operations with deprecated verbs raise HarnessDeprecatedEndpointError
        '''
        # Mock the HTTP client to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        
        # Create a HarnessApiClient with minimal config
        client = HarnessApiClient({
            'apikey': 'test-apikey',
            'harness_token': 'test-harness-token'
        })
        
        # Mock the _is_deprecated_endpoint method to properly check for deprecated endpoints
        original_is_deprecated = client._workspace_client._http_client._is_deprecated_endpoint
        client._workspace_client._http_client._is_deprecated_endpoint = original_is_deprecated
        
        # Test creating a workspace (POST) - should be deprecated
        with pytest.raises(HarnessDeprecatedEndpointError):
            client.workspaces.add({
                'name': 'Test Workspace',
                'requiresTitleAndComments': False
            })
        
        # Test updating a workspace (PATCH) - should be deprecated
        with pytest.raises(HarnessDeprecatedEndpointError):
            client.workspaces.update('ws-1', 'name', 'Updated Workspace')
        
        # Test deleting a workspace (DELETE) - should be deprecated
        with pytest.raises(HarnessDeprecatedEndpointError):
            client.workspaces.delete('ws-1')
        
        # Test listing workspaces (GET) - should be allowed
        # Mock a successful response
        from splitapiclient.resources import Workspace
        mock_response = {
            'objects': [
                {
                    'id': 'ws-1',
                    'name': 'Workspace 1',
                    'requiresTitleAndComments': False
                }
            ],
            'offset': 0,
            'totalCount': 1,
            'limit': 10
        }
        client._workspace_client._http_client.make_request.return_value = mock_response
        
        # This should not raise an exception
        workspaces = client.workspaces.list()
        assert len(workspaces) == 1
        assert isinstance(workspaces[0], Workspace)
    
    def test_apikeys_admin_restrictions(self, mocker):
        '''
        Test that apikey operations with admin type and deprecated verbs raise HarnessDeprecatedEndpointError
        '''
        # Mock the HTTP client to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        
        # Create a HarnessApiClient with minimal config
        client = HarnessApiClient({
            'apikey': 'test-apikey',
            'harness_token': 'test-harness-token'
        })
        
        # Mock the _is_deprecated_endpoint method to properly check for deprecated endpoints
        original_is_deprecated = client._apikey_client._http_client._is_deprecated_endpoint
        client._apikey_client._http_client._is_deprecated_endpoint = original_is_deprecated
        
        # Test creating an admin API key (POST) - should be deprecated
        with pytest.raises(HarnessDeprecatedEndpointError):
            client.apikeys.add({
                'name': 'Admin API Key',
                'type': 'admin'
            })
        
        # Test creating a non-admin API key (POST) - should be allowed
        # Mock a successful response
        from splitapiclient.resources import APIKey
        mock_response = {
            'id': 'key-1',
            'name': 'Client API Key',
            'type': 'client'
        }
        client._apikey_client._http_client.make_request.return_value = mock_response
        
        # This should not raise an exception
        apikey = client.apikeys.add({
            'name': 'Client API Key',
            'type': 'client'
        })
        assert isinstance(apikey, APIKey)
        assert apikey.name == 'Client API Key'
    
    def test_users_restrictions(self, mocker):
        '''
        Test that all user operations raise HarnessDeprecatedEndpointError
        '''
        # Mock the HTTP client to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        
        # Create a HarnessApiClient with minimal config
        client = HarnessApiClient({
            'apikey': 'test-apikey',
            'harness_token': 'test-harness-token'
        })
        
        # Mock the _is_deprecated_endpoint method to properly check for deprecated endpoints
        original_is_deprecated = client._identity_client._http_client._is_deprecated_endpoint
        client._identity_client._http_client._is_deprecated_endpoint = original_is_deprecated
        
        # Test listing users (GET) - should be deprecated
        with pytest.raises(HarnessDeprecatedEndpointError):
            client.identities.list()
        
        # Test getting a user (GET) - should be deprecated
        with pytest.raises(HarnessDeprecatedEndpointError):
            client.identities.get('user-1')
        
        # Test creating a user (POST) - should be deprecated
        with pytest.raises(HarnessDeprecatedEndpointError):
            client.identities.add({
                'name': 'Test User',
                'email': 'test@example.com'
            })
        
        # Test updating a user (PATCH) - should be deprecated
        with pytest.raises(HarnessDeprecatedEndpointError):
            client.identities.update('user-1', 'name', 'Updated User')
        
        # Test deleting a user (DELETE) - should be deprecated
        with pytest.raises(HarnessDeprecatedEndpointError):
            client.identities.delete('user-1')
    
    def test_groups_restrictions(self, mocker):
        '''
        Test that all group operations raise HarnessDeprecatedEndpointError
        '''
        # Mock the HTTP client to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        
        # Create a HarnessApiClient with minimal config
        client = HarnessApiClient({
            'apikey': 'test-apikey',
            'harness_token': 'test-harness-token'
        })
        
        # Test group operations - all should be deprecated
        # Note: We're using the harness_group client here which is a different client
        # than the one used for Split groups, but we should test both
        
        # Test using the Split groups client
        with pytest.raises(HarnessDeprecatedEndpointError):
            # This would call the deprecated Split groups endpoint
            client._group_client._http_client.make_request({
                'method': 'GET',
                'url_template': 'groups',
                'headers': [],
                'query_string': [],
                'response': True
            })
        
        # Test using the Harness groups client
        # This should work fine because it uses the Harness-specific endpoint
        # Mock a successful response
        from splitapiclient.resources.harness import HarnessGroup
        mock_response = {
            'identifier': 'group-1',
            'name': 'Harness Group 1'
        }
        client._harness_group_client._http_client.make_request.return_value = mock_response
        
        # This should not raise an exception because it's using the Harness-specific endpoint
        group = client.harness_group.get('group-1')
        assert isinstance(group, HarnessGroup)
        assert group.name == 'Harness Group 1'
    
    def test_restrictions_restrictions(self, mocker):
        '''
        Test that all restrictions operations raise HarnessDeprecatedEndpointError
        '''
        # Mock the HTTP client to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        
        # Create a HarnessApiClient with minimal config
        client = HarnessApiClient({
            'apikey': 'test-apikey',
            'harness_token': 'test-harness-token'
        })
        
        # Test restrictions operations - all should be deprecated
        with pytest.raises(HarnessDeprecatedEndpointError):
            # This would call the deprecated restrictions endpoint
            client._http_client.make_request({
                'method': 'GET',
                'url_template': 'restrictions',
                'headers': [],
                'query_string': [],
                'response': True
            })
    
    def test_harness_specific_endpoints(self, mocker):
        '''
        Test that Harness-specific endpoints are not restricted
        '''
        # Mock the HTTP client to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        
        # Create a HarnessApiClient with minimal config
        client = HarnessApiClient({
            'apikey': 'test-apikey',
            'harness_token': 'test-harness-token'
        })
        
        # Mock successful responses for Harness-specific endpoints
        # Token
        token_response = {
            'identifier': 'token-1',
            'name': 'Token 1'
        }
        client._token_client._http_client.make_request.return_value = token_response
        
        # HarnessApiKey
        apikey_response = {
            'identifier': 'apikey-1',
            'name': 'API Key 1'
        }
        client._harness_apikey_client._http_client.make_request.return_value = apikey_response
        
        # ServiceAccount
        sa_response = {
            'identifier': 'sa-1',
            'name': 'Service Account 1'
        }
        client._service_account_client._http_client.make_request.return_value = sa_response
        
        # HarnessProject
        project_response = {
            'identifier': 'project-1',
            'name': 'Project 1'
        }
        client._harness_project_client._http_client.make_request.return_value = project_response
        
        # These should not raise exceptions
        token = client.token.get('token-1')
        assert token.identifier == 'token-1'
        
        apikey = client.harness_apikey.get('apikey-1')
        assert apikey.identifier == 'apikey-1'
        
        sa = client.service_account.get('sa-1')
        assert sa.identifier == 'sa-1'
        
        project = client.harness_project.get('project-1')
        assert project.identifier == 'project-1'
