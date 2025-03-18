from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients.harness import HarnessApiKeyMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources.harness import HarnessApiKey


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
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['all_items'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['all_items'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['get_apikey'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['get_apikey'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['create'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['add_permissions'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['delete'],
            apiKeyIdentifier='apikey1',
            accountIdentifier='test_account',
            parentIdentifier='parent1'
        )
        
        # Verify the result
        assert result is True
