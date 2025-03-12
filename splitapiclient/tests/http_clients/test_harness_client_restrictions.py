from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.util.exceptions import HarnessDeprecatedEndpointError


class TestHarnessClientRestrictions:
    '''
    Tests to verify that deprecated endpoints in Harness mode raise HarnessDeprecatedEndpointError
    '''
    
    def test_workspaces_deprecated_verbs(self, mocker):
        '''
        Test that POST, PATCH, DELETE, PUT verbs on /workspaces endpoint raise HarnessDeprecatedEndpointError
        '''
        # Mock requests to avoid actual HTTP calls
        mocker.patch('requests.post')
        mocker.patch('requests.patch')
        mocker.patch('requests.delete')
        mocker.patch('requests.put')
        
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        
        # Define endpoints with deprecated verbs
        post_endpoint = {
            'method': 'POST',
            'url_template': 'workspaces',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        patch_endpoint = {
            'method': 'PATCH',
            'url_template': 'workspaces/ws1',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        delete_endpoint = {
            'method': 'DELETE',
            'url_template': 'workspaces/ws1',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        put_endpoint = {
            'method': 'PUT',
            'url_template': 'workspaces/ws1',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        # Test each deprecated verb
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(post_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(patch_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(delete_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(put_endpoint)
        
        # Verify that GET is still allowed
        get_endpoint = {
            'method': 'GET',
            'url_template': 'workspaces',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        # Mock the response for GET
        mocker.patch.object(http_client, '_setup_url', return_value='https://app.harness.io/gateway/ff/api/v2/workspaces')
        mocker.patch.object(http_client, '_setup_headers', return_value={})
        
        # Create a mock response
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = '{"items": []}'
        mocker.patch('requests.get', return_value=mock_response)
        
        # This should not raise an exception
        result = http_client.make_request(get_endpoint)
        assert result is not None
    
    def test_apikeys_admin_deprecated_verbs(self, mocker):
        '''
        Test that POST and DELETE verbs on /apiKeys endpoint with apiKeyType=admin raise HarnessDeprecatedEndpointError
        '''
        # Mock requests to avoid actual HTTP calls
        mocker.patch('requests.post')
        mocker.patch('requests.delete')
        
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        
        # Define endpoints with deprecated verbs and admin apiKeyType
        post_endpoint = {
            'method': 'POST',
            'url_template': 'apiKeys',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        delete_endpoint = {
            'method': 'DELETE',
            'url_template': 'apiKeys/key1',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        # Test POST with admin apiKeyType
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(post_endpoint, body={'apiKeyType': 'admin'})
        
        # Test DELETE with admin apiKeyType (in this case, the body is not used for the check,
        # but we would need to mock the API to check the apiKeyType of the key being deleted)
        
        # Verify that POST with non-admin apiKeyType is allowed
        # Mock the response for POST
        mocker.patch.object(http_client, '_setup_url', return_value='https://app.harness.io/gateway/ff/api/v2/apiKeys')
        mocker.patch.object(http_client, '_setup_headers', return_value={})
        
        # Create a mock response
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = '{"identifier": "key1"}'
        mocker.patch('requests.post', return_value=mock_response)
        
        # This should not raise an exception
        result = http_client.make_request(post_endpoint, body={'apiKeyType': 'client'})
        assert result is not None
    
    def test_users_all_verbs_deprecated(self, mocker):
        '''
        Test that all verbs on /users endpoint raise HarnessDeprecatedEndpointError
        '''
        # Mock requests to avoid actual HTTP calls
        mocker.patch('requests.get')
        mocker.patch('requests.post')
        mocker.patch('requests.patch')
        mocker.patch('requests.delete')
        
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        
        # Define endpoints for different verbs
        get_endpoint = {
            'method': 'GET',
            'url_template': 'users',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        post_endpoint = {
            'method': 'POST',
            'url_template': 'users',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        patch_endpoint = {
            'method': 'PATCH',
            'url_template': 'users/user1',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        delete_endpoint = {
            'method': 'DELETE',
            'url_template': 'users/user1',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        # Test each verb
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(get_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(post_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(patch_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(delete_endpoint)
    
    def test_groups_all_verbs_deprecated(self, mocker):
        '''
        Test that all verbs on /groups endpoint raise HarnessDeprecatedEndpointError
        '''
        # Mock requests to avoid actual HTTP calls
        mocker.patch('requests.get')
        mocker.patch('requests.post')
        mocker.patch('requests.patch')
        mocker.patch('requests.delete')
        
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        
        # Define endpoints for different verbs
        get_endpoint = {
            'method': 'GET',
            'url_template': 'groups',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        post_endpoint = {
            'method': 'POST',
            'url_template': 'groups',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        patch_endpoint = {
            'method': 'PATCH',
            'url_template': 'groups/group1',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        delete_endpoint = {
            'method': 'DELETE',
            'url_template': 'groups/group1',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        # Test each verb
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(get_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(post_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(patch_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(delete_endpoint)
    
    def test_restrictions_all_verbs_deprecated(self, mocker):
        '''
        Test that all verbs on /restrictions endpoint raise HarnessDeprecatedEndpointError
        '''
        # Mock requests to avoid actual HTTP calls
        mocker.patch('requests.get')
        mocker.patch('requests.post')
        mocker.patch('requests.patch')
        mocker.patch('requests.delete')
        
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        
        # Define endpoints for different verbs
        get_endpoint = {
            'method': 'GET',
            'url_template': 'restrictions',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        post_endpoint = {
            'method': 'POST',
            'url_template': 'restrictions',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        patch_endpoint = {
            'method': 'PATCH',
            'url_template': 'restrictions/restriction1',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        delete_endpoint = {
            'method': 'DELETE',
            'url_template': 'restrictions/restriction1',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        # Test each verb
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(get_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(post_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(patch_endpoint)
        
        with pytest.raises(HarnessDeprecatedEndpointError):
            http_client.make_request(delete_endpoint)
    
    def test_non_deprecated_endpoints(self, mocker):
        '''
        Test that non-deprecated endpoints do not raise HarnessDeprecatedEndpointError
        '''
        # Mock requests to avoid actual HTTP calls
        mocker.patch('requests.get')
        mocker.patch('requests.post')
        
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        
        # Mock the response setup
        mocker.patch.object(http_client, '_setup_url', return_value='https://app.harness.io/gateway/ff/api/v2/tokens')
        mocker.patch.object(http_client, '_setup_headers', return_value={})
        
        # Create a mock response
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = '{"items": []}'
        mocker.patch('requests.get', return_value=mock_response)
        
        # Define non-deprecated endpoints
        tokens_get_endpoint = {
            'method': 'GET',
            'url_template': 'tokens',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        tokens_post_endpoint = {
            'method': 'POST',
            'url_template': 'tokens',
            'headers': [],
            'query_string': [],
            'response': True
        }
        
        # These should not raise exceptions
        result = http_client.make_request(tokens_get_endpoint)
        assert result is not None
        
        mock_response.text = '{"identifier": "token1"}'
        mocker.patch('requests.post', return_value=mock_response)
        
        result = http_client.make_request(tokens_post_endpoint)
        assert result is not None
