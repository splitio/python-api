from __future__ import absolute_import, division, print_function, \
    unicode_literals

import json
from splitapiclient.microclients.harness import HarnessApiKeyMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import HarnessApiKey
from splitapiclient.tests.microclients.harness.conftest import FakeResponse


class TestHarnessApiKeyMicroClient:

    def test_list(self, mocker):
        '''
        Test listing API keys
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        akmc = HarnessApiKeyMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': [
                {
                    'identifier': 'apikey1',
                    'name': 'API Key 1',
                    'description': 'Test API key 1',
                    'accountIdentifier': 'test_account',
                    'parentIdentifier': 'parent1',
                    'apiKeyType': 'SERVICE_ACCOUNT'
                },
                {
                    'identifier': 'apikey2',
                    'name': 'API Key 2',
                    'description': 'Test API key 2',
                    'accountIdentifier': 'test_account',
                    'parentIdentifier': 'parent1',
                    'apiKeyType': 'SERVICE_ACCOUNT'
                }
            ]
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = akmc.list('parent1')
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessApiKeyMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/ng/api/apikey?accountIdentifier={accountIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            accountIdentifier='test_account',
            parentIdentifier='parent1'
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], HarnessApiKey)
        assert isinstance(result[1], HarnessApiKey)
        assert result[0]._identifier == 'apikey1'
        assert result[1]._identifier == 'apikey2'

    def test_list_empty_parent(self, mocker):
        '''
        Test listing API keys with empty parent identifier
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        akmc = HarnessApiKeyMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': []
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = akmc.list()
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessApiKeyMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/ng/api/apikey?accountIdentifier={accountIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            accountIdentifier='test_account',
            parentIdentifier=""
        )
        
        # Verify the result
        assert len(result) == 0

    def test_get(self, mocker):
        '''
        Test getting a specific API key
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        akmc = HarnessApiKeyMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': {
                'apiKey': {
                    'identifier': 'apikey1',
                    'name': 'API Key 1',
                    'description': 'Test API key 1',
                    'accountIdentifier': 'test_account',
                    'parentIdentifier': 'parent1',
                    'apiKeyType': 'SERVICE_ACCOUNT'
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = akmc.get('apikey1', 'parent1')
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessApiKeyMicroClient._endpoint['get_apikey'].copy()
        expected_endpoint['url_template'] = '/ng/api/apikey/aggregate/{apiKeyIdentifier}?accountIdentifier={accountIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            apiKeyIdentifier='apikey1',
            accountIdentifier='test_account',
            parentIdentifier='parent1'
        )
        
        # Verify the result
        assert isinstance(result, HarnessApiKey)
        assert result._identifier == 'apikey1'
        assert result._name == 'API Key 1'
        assert result._description == 'Test API key 1'

    def test_get_not_found(self, mocker):
        '''
        Test getting a non-existent API key
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        akmc = HarnessApiKeyMicroClient(sc, 'test_account')
        
        # Mock the API response for a non-existent key
        response_data = {
            'data': {}
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = akmc.get('nonexistent', 'parent1')
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessApiKeyMicroClient._endpoint['get_apikey'].copy()
        expected_endpoint['url_template'] = '/ng/api/apikey/aggregate/{apiKeyIdentifier}?accountIdentifier={accountIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            apiKeyIdentifier='nonexistent',
            accountIdentifier='test_account',
            parentIdentifier='parent1'
        )
        
        # Verify the result
        assert result is None

    def test_create(self, mocker):
        '''
        Test creating an API key
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        akmc = HarnessApiKeyMicroClient(sc, 'test_account')
        
        # API key data to create
        apikey_data = {
            'name': 'New API Key',
            'description': 'Test API key',
            'parentIdentifier': 'parent1',
            'apiKeyType': 'SERVICE_ACCOUNT'
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'identifier': 'new_apikey',
                'name': 'New API Key',
                'description': 'Test API key',
                'accountIdentifier': 'test_account',
                'parentIdentifier': 'parent1',
                'apiKeyType': 'SERVICE_ACCOUNT',
                'createdAt': 1234567890,
                'lastModifiedAt': 1234567890
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = akmc.create(apikey_data)
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessApiKeyMicroClient._endpoint['create'].copy()
        expected_endpoint['url_template'] = '/ng/api/apikey?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            body=apikey_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, HarnessApiKey)
        assert result._identifier == 'new_apikey'
        assert result._name == 'New API Key'
        assert result._description == 'Test API key'

    def test_add_permissions(self, mocker):
        '''
        Test adding permissions to an API key
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        akmc = HarnessApiKeyMicroClient(sc, 'test_account')
        
        # Permissions data
        permissions = {
            'roleAssignments': [
                {
                    'roleIdentifier': 'role1',
                    'resourceGroupIdentifier': 'resourceGroup1',
                    'principal': {
                        'identifier': 'apikey1',
                        'type': 'SERVICE_ACCOUNT'
                    }
                }
            ]
        }
        
        # Mock the API response
        response_data = {
            'data': True
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = akmc.add_permissions('apikey1', permissions)
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessApiKeyMicroClient._endpoint['add_permissions'].copy()
        expected_endpoint['url_template'] = '/ng/api/roleassignments?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            body=permissions,
            apiKeyIdentifier='apikey1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True

    def test_delete(self, mocker):
        '''
        Test deleting an API key
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        akmc = HarnessApiKeyMicroClient(sc, 'test_account')
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = {}
        
        # Call the method being tested
        result = akmc.delete('apikey1', 'parent1')
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessApiKeyMicroClient._endpoint['delete'].copy()
        expected_endpoint['url_template'] = '/ng/api/apikey/{apiKeyIdentifier}?accountIdentifier={accountIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            apiKeyIdentifier='apikey1',
            accountIdentifier='test_account',
            parentIdentifier='parent1'
        )
        
        # Verify the result
        assert result is True


class TestHarnessApiKeyURLGeneration:
    """
    Tests that verify actual URL generation by mocking at the requests level.
    These tests ensure that optional parameters (orgIdentifier, projectIdentifier)
    are correctly included or excluded from the final URL.
    """

    # =========================================================================
    # LIST method URL tests
    # =========================================================================

    def test_list_url_without_optional_identifiers(self, mocker):
        """Verify list URL doesn't contain orgIdentifier/projectIdentifier when not set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({'data': []}))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessApiKeyMicroClient(hc, 'test_account')
        client.list('parent1')

        called_url = mock_get.call_args[0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'parentIdentifier=parent1' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_org_identifier_only(self, mocker):
        """Verify list URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({'data': []}))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessApiKeyMicroClient(hc, 'test_account', org_identifier='org1')
        client.list('parent1')

        called_url = mock_get.call_args[0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'parentIdentifier=parent1' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_project_identifier_only(self, mocker):
        """Verify list URL contains projectIdentifier when set, but not orgIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({'data': []}))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessApiKeyMicroClient(hc, 'test_account', project_identifier='proj1')
        client.list('parent1')

        called_url = mock_get.call_args[0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'parentIdentifier=parent1' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier=proj1' in called_url

    def test_list_url_with_both_identifiers(self, mocker):
        """Verify list URL contains both orgIdentifier and projectIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({'data': []}))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessApiKeyMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.list('parent1')

        called_url = mock_get.call_args[0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'parentIdentifier=parent1' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url

    def test_list_url_with_method_override_identifiers(self, mocker):
        """Verify list URL uses method parameters to override instance defaults"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({'data': []}))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessApiKeyMicroClient(hc, 'test_account', org_identifier='default_org', project_identifier='default_proj')
        client.list('parent1', org_identifier='override_org', project_identifier='override_proj')

        called_url = mock_get.call_args[0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=override_org' in called_url
        assert 'projectIdentifier=override_proj' in called_url
        assert 'default_org' not in called_url
        assert 'default_proj' not in called_url

    # =========================================================================
    # GET method URL tests
    # =========================================================================

    def test_get_url_without_optional_identifiers(self, mocker):
        """Verify get URL doesn't contain orgIdentifier/projectIdentifier when not set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'apiKey': {'identifier': 'ak1', 'name': 'AK1', 'description': '', 'parentIdentifier': 'parent1', 'apiKeyType': 'SERVICE_ACCOUNT'}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessApiKeyMicroClient(hc, 'test_account')
        client.get('ak1', 'parent1')

        called_url = mock_get.call_args[0][0]
        assert '/apikey/aggregate/ak1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'parentIdentifier=parent1' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_org_identifier_only(self, mocker):
        """Verify get URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'apiKey': {'identifier': 'ak1', 'name': 'AK1', 'description': '', 'parentIdentifier': 'parent1', 'apiKeyType': 'SERVICE_ACCOUNT'}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessApiKeyMicroClient(hc, 'test_account', org_identifier='org1')
        client.get('ak1', 'parent1')

        called_url = mock_get.call_args[0][0]
        assert '/apikey/aggregate/ak1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'parentIdentifier=parent1' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_both_identifiers(self, mocker):
        """Verify get URL contains both orgIdentifier and projectIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'apiKey': {'identifier': 'ak1', 'name': 'AK1', 'description': '', 'parentIdentifier': 'parent1', 'apiKeyType': 'SERVICE_ACCOUNT'}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessApiKeyMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.get('ak1', 'parent1')

        called_url = mock_get.call_args[0][0]
        assert '/apikey/aggregate/ak1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'parentIdentifier=parent1' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url
