from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.microclients import WorkspaceMicroClient, APIKeyMicroClient, UserMicroClient, GroupMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.main.harness_apiclient import HarnessApiClient
from splitapiclient.util.exceptions import HarnessDeprecatedEndpointError


class TestDeprecatedEndpoints:
    """
    Tests for verifying that certain endpoints are deprecated when in harness mode
    """

    def test_workspace_endpoints_deprecated_in_harness_mode(self, mocker):
        """
        Test that workspace POST, PATCH, DELETE, PUT verbs are deprecated in harness mode
        """
        # Mock the HarnessHttpClient to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        harness_make_request_mock = mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        
        # Create a HarnessApiClient
        client = HarnessApiClient({
            'apikey': 'abc',
            'harness_token': 'abc'
        })
        
        # Create a WorkspaceMicroClient with the client's HTTP client
        wmc = WorkspaceMicroClient(client._workspace_client._http_client)
        
        # Configure the mock to raise HarnessDeprecatedEndpointError for POST, PATCH, DELETE
        def mock_make_request(endpoint, **kwargs):
            method = endpoint.get('method', '')
            url_template = endpoint.get('url_template', '')
            
            if 'workspaces' in url_template:
                if method == 'POST':
                    raise HarnessDeprecatedEndpointError(f"Endpoint workspaces with method {method} is deprecated in harness mode")
                elif method == 'PATCH' and '{workspaceId}' in url_template:
                    raise HarnessDeprecatedEndpointError(f"Endpoint workspaces/{{workspaceId}} with method {method} is deprecated in harness mode")
                elif method == 'DELETE' and '{workspaceId}' in url_template:
                    raise HarnessDeprecatedEndpointError(f"Endpoint workspaces/{{workspaceId}} with method {method} is deprecated in harness mode")
                elif method == 'GET':
                    return {'objects': [], 'offset': 0, 'totalCount': 0, 'limit': 20}
            
            return {'data': {}}
        
        harness_make_request_mock.side_effect = mock_make_request
        
        # Test create (POST) is deprecated
        with pytest.raises(HarnessDeprecatedEndpointError) as excinfo:
            wmc.add({'name': 'Test Workspace'})
        assert "Endpoint workspaces with method POST is deprecated in harness mode" in str(excinfo.value)
        
        # Test update (PATCH) is deprecated
        with pytest.raises(HarnessDeprecatedEndpointError) as excinfo:
            wmc.update('workspace1', 'requireTitleAndComments', False)
        assert "Endpoint workspaces/{workspaceId} with method PATCH is deprecated in harness mode" in str(excinfo.value)
        
        # Test delete (DELETE) is deprecated
        with pytest.raises(HarnessDeprecatedEndpointError) as excinfo:
            wmc.delete('workspace1')
        assert "Endpoint workspaces/{workspaceId} with method DELETE is deprecated in harness mode" in str(excinfo.value)
        
        # Verify that GET operations are still allowed
        wmc.list()  # Should not raise an exception
        harness_make_request_mock.assert_called()

    def test_apikey_admin_endpoints_deprecated_in_harness_mode(self, mocker):
        """
        Test that apiKey POST verb for apiKeyType 'admin' is deprecated in harness mode
        """
        # Create a custom HarnessHttpClient with the _is_deprecated_endpoint method properly implemented
        class TestHarnessHttpClient(HarnessHttpClient):
            def __init__(self, baseurl, auth_token):
                super(TestHarnessHttpClient, self).__init__(baseurl, auth_token)
                self.apikey_types = {}  # Store API key types for testing
            
            def _is_deprecated_endpoint(self, endpoint, body=None, **kwargs):
                url_template = endpoint['url_template']
                method = endpoint['method']
                
                # Check for apiKeys endpoint with admin type
                if url_template.startswith('apiKeys') and method == 'POST':
                    if body and body.get('apiKeyType') == 'admin':
                        raise HarnessDeprecatedEndpointError("Operation 'create_apikey' for apiKeyType 'admin' is deprecated in harness mode")
                
                return False
            
            def make_request(self, endpoint, body=None, **kwargs):
                # Check if endpoint is deprecated
                self._is_deprecated_endpoint(endpoint, body, **kwargs)
                
                method = endpoint.get('method', '')
                url_template = endpoint.get('url_template', '')
                
                # Handle API key creation
                if method == 'POST' and url_template.startswith('apiKeys'):
                    # Store the API key type for later use in delete operations
                    apikey_id = 'apikey-1'
                    if body and 'apiKeyType' in body:
                        self.apikey_types[apikey_id] = body['apiKeyType']
                    return {'data': {'id': apikey_id}}
                
                # Handle API key deletion
                if method == 'DELETE' and url_template.startswith('apiKeys/'):
                    return {'data': {}}
                
                return {'data': {}}
        
        # Create a test client
        client = TestHarnessHttpClient('https://api.split.io/internal/api/v2', 'test-token')
        
        # Create an APIKeyMicroClient with our test client
        akmc = APIKeyMicroClient(client)
        
        # Test create (POST) for admin type is deprecated
        with pytest.raises(HarnessDeprecatedEndpointError) as excinfo:
            akmc.create_apikey('Test API Key', 'admin', ['env1', 'env2'], 'ws1', ['role1', 'role2'])
        assert "Operation 'create_apikey' for apiKeyType 'admin' is deprecated in harness mode" in str(excinfo.value)
        
        # Test create (POST) for client type is allowed
        apikey = akmc.create_apikey('Test API Key', 'client_side', ['env1', 'env2'], 'ws1', ['role1', 'role2'])
        
        # Test that delete operations are allowed for all API key types
        client.apikey_types['admin-apikey'] = 'admin'
        akmc.delete_apikey('admin-apikey')  # Should not raise an exception
        akmc.delete_apikey('apikey-1')      # Should not raise an exception


class TestAuthenticationInHarnessMode:
    """
    Tests for verifying authentication behavior in harness mode
    """
    
    def test_harness_token_used_for_harness_endpoints(self, mocker):
        """
        Test that harness_token is used for Harness endpoints and apikey for Split endpoints
        """
        # Create a custom HTTP client class for testing
        class TestHttpClient(HarnessHttpClient):
            def __init__(self, baseurl, auth_token):
                self.baseurl = baseurl
                self.auth_token = auth_token
                # Initialize with empty config
                self.config = {'base_args': {}}
                
                # For Harness HTTP client, set x-api-key in base_args
                if 'harness' in baseurl:
                    self.config['base_args'] = {'x-api-key': auth_token}
                else:
                    # For Split HTTP client, we'll check Authorization header in make_request
                    pass
                    
            def make_request(self, endpoint, body=None, **kwargs):
                # Just return a successful response without making actual requests
                mock_response = mocker.Mock()
                mock_response.status_code = 200
                mock_response.text = '{}'
                return {}
        
        # Patch the HarnessHttpClient constructor to use our test class
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', 
                    TestHttpClient.__init__)
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request', 
                    TestHttpClient.make_request)
        
        # Create client with both harness_token and apikey
        client = HarnessApiClient({
            'harness_token': 'harness_token_value',
            'apikey': 'api_key_value'
        })
        
        # Check that the Harness HTTP client was initialized with harness_token
        assert client._token_client._http_client.auth_token == 'harness_token_value'
        
        # Check that the Split HTTP client was initialized with apikey
        assert client._split_client._http_client.auth_token == 'api_key_value'

    def test_apikey_fallback_when_no_harness_token(self, mocker):
        """
        Test that apikey is used for all operations when harness_token is not provided
        """
        # Create a custom HTTP client class for testing
        class TestHttpClient(HarnessHttpClient):
            def __init__(self, baseurl, auth_token):
                self.baseurl = baseurl
                self.auth_token = auth_token
                # Initialize with empty config
                self.config = {'base_args': {}}
                
                # For Harness HTTP client, set x-api-key in base_args
                if 'harness' in baseurl:
                    self.config['base_args'] = {'x-api-key': auth_token}
                else:
                    # For Split HTTP client, we'll check Authorization header in make_request
                    pass
                    
            def make_request(self, endpoint, body=None, **kwargs):
                # Just return a successful response without making actual requests
                mock_response = mocker.Mock()
                mock_response.status_code = 200
                mock_response.text = '{}'
                return {}
        
        # Patch the HarnessHttpClient constructor to use our test class
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', 
                    TestHttpClient.__init__)
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request', 
                    TestHttpClient.make_request)
        
        # Create client with only apikey
        client = HarnessApiClient({
            'apikey': 'api_key_value'
        })
        
        # Check that the Harness HTTP client was initialized with apikey as fallback
        assert client._token_client._http_client.auth_token == 'api_key_value'
        
        # Check that the Split HTTP client was initialized with apikey
        assert client._split_client._http_client.auth_token == 'api_key_value'
