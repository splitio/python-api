from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.microclients.harness import HarnessApiKeyMicroClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import HarnessApiKey


class TestHarnessApiKeyMicroClient:
    '''
    Tests for the HarnessApiKeyMicroClient class' methods
    '''
    
    def test_list(self, mocker):
        '''
        Test that the list method properly returns a list of HarnessApiKey objects
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        apikey_client = HarnessApiKeyMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'items': [
                {
                    'identifier': 'apikey-1',
                    'name': 'API Key 1',
                    'apiKeyType': 'CLIENT',
                    'accountIdentifier': 'account-1'
                },
                {
                    'identifier': 'apikey-2',
                    'name': 'API Key 2',
                    'apiKeyType': 'CLIENT',
                    'accountIdentifier': 'account-1'
                }
            ]
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = apikey_client.list()
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['all_items'],
            query_params={}
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], HarnessApiKey)
        assert result[0].identifier == 'apikey-1'
        assert result[0].name == 'API Key 1'
        assert result[1].identifier == 'apikey-2'
        assert result[1].name == 'API Key 2'
    
    def test_list_with_filters(self, mocker):
        '''
        Test that the list method properly handles account, org, and project filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        apikey_client = HarnessApiKeyMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'items': [
                {
                    'identifier': 'apikey-1',
                    'name': 'API Key 1',
                    'apiKeyType': 'CLIENT',
                    'accountIdentifier': 'account-1',
                    'orgIdentifier': 'org-1',
                    'projectIdentifier': 'project-1'
                }
            ]
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method with filters
        result = apikey_client.list(account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['all_items'],
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert len(result) == 1
        assert result[0].identifier == 'apikey-1'
        assert result[0].account_identifier == 'account-1'
        assert result[0].org_identifier == 'org-1'
        assert result[0].project_identifier == 'project-1'
    
    def test_get(self, mocker):
        '''
        Test that the get method properly returns a HarnessApiKey object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        apikey_client = HarnessApiKeyMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'identifier': 'apikey-1',
            'name': 'API Key 1',
            'apiKeyType': 'CLIENT',
            'accountIdentifier': 'account-1'
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = apikey_client.get('apikey-1')
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['get_apikey'],
            apiKeyId='apikey-1',
            query_params={}
        )
        
        # Verify the result
        assert isinstance(result, HarnessApiKey)
        assert result.identifier == 'apikey-1'
        assert result.name == 'API Key 1'
        assert result.api_key_type == 'CLIENT'
        assert result.account_identifier == 'account-1'
    
    def test_get_with_filters(self, mocker):
        '''
        Test that the get method properly handles account, org, and project filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        apikey_client = HarnessApiKeyMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'identifier': 'apikey-1',
            'name': 'API Key 1',
            'apiKeyType': 'CLIENT',
            'accountIdentifier': 'account-1',
            'orgIdentifier': 'org-1',
            'projectIdentifier': 'project-1'
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method with filters
        result = apikey_client.get('apikey-1', account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['get_apikey'],
            apiKeyId='apikey-1',
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert result.identifier == 'apikey-1'
        assert result.account_identifier == 'account-1'
        assert result.org_identifier == 'org-1'
        assert result.project_identifier == 'project-1'
    
    def test_create(self, mocker):
        '''
        Test that the create method properly creates and returns a HarnessApiKey object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        apikey_client = HarnessApiKeyMicroClient(http_client)
        
        # API Key data to create
        apikey_data = {
            'name': 'New API Key',
            'description': 'A new API key',
            'apiKeyType': 'CLIENT',
            'accountIdentifier': 'account-1',
            'orgIdentifier': 'org-1',
            'projectIdentifier': 'project-1'
        }
        
        # Mock response data (usually the same as input but with additional fields)
        response_data = apikey_data.copy()
        response_data['identifier'] = 'apikey-new'
        response_data['createdAt'] = 1615000000000
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = apikey_client.create(apikey_data)
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['create'],
            body=apikey_data
        )
        
        # Verify the result
        assert isinstance(result, HarnessApiKey)
        assert result.identifier == 'apikey-new'
        assert result.name == 'New API Key'
        assert result.description == 'A new API key'
        assert result.api_key_type == 'CLIENT'
        assert result.account_identifier == 'account-1'
        assert result.org_identifier == 'org-1'
        assert result.project_identifier == 'project-1'
        assert result.created_at == 1615000000000
    
    def test_update(self, mocker):
        '''
        Test that the update method properly updates and returns a HarnessApiKey object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        apikey_client = HarnessApiKeyMicroClient(http_client)
        
        # API Key data to update
        apikey_data = {
            'name': 'Updated API Key',
            'description': 'An updated API key'
        }
        
        # Mock response data (usually the same as input but with all fields)
        response_data = apikey_data.copy()
        response_data['identifier'] = 'apikey-1'
        response_data['apiKeyType'] = 'CLIENT'
        response_data['accountIdentifier'] = 'account-1'
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = apikey_client.update('apikey-1', apikey_data)
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['update'],
            apiKeyId='apikey-1',
            body=apikey_data,
            query_params={}
        )
        
        # Verify the result
        assert isinstance(result, HarnessApiKey)
        assert result.identifier == 'apikey-1'
        assert result.name == 'Updated API Key'
        assert result.description == 'An updated API key'
        assert result.api_key_type == 'CLIENT'
        assert result.account_identifier == 'account-1'
    
    def test_update_with_filters(self, mocker):
        '''
        Test that the update method properly handles account, org, and project filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        apikey_client = HarnessApiKeyMicroClient(http_client)
        
        # API Key data to update
        apikey_data = {
            'name': 'Updated API Key',
            'description': 'An updated API key'
        }
        
        # Mock response data
        response_data = apikey_data.copy()
        response_data['identifier'] = 'apikey-1'
        response_data['apiKeyType'] = 'CLIENT'
        response_data['accountIdentifier'] = 'account-1'
        response_data['orgIdentifier'] = 'org-1'
        response_data['projectIdentifier'] = 'project-1'
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method with filters
        result = apikey_client.update('apikey-1', apikey_data, account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['update'],
            apiKeyId='apikey-1',
            body=apikey_data,
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert result.identifier == 'apikey-1'
        assert result.name == 'Updated API Key'
        assert result.account_identifier == 'account-1'
        assert result.org_identifier == 'org-1'
        assert result.project_identifier == 'project-1'
    
    def test_delete(self, mocker):
        '''
        Test that the delete method properly deletes an API key
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        apikey_client = HarnessApiKeyMicroClient(http_client)
        
        # Mock response data (usually empty for delete operations)
        HarnessHttpClient.make_request.return_value = None
        
        # Call the method
        result = apikey_client.delete('apikey-1')
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['delete'],
            apiKeyId='apikey-1',
            query_params={}
        )
        
        # Verify the result
        assert result is True
    
    def test_delete_with_filters(self, mocker):
        '''
        Test that the delete method properly handles account, org, and project filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        apikey_client = HarnessApiKeyMicroClient(http_client)
        
        # Mock response data (usually empty for delete operations)
        HarnessHttpClient.make_request.return_value = None
        
        # Call the method with filters
        result = apikey_client.delete('apikey-1', account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessApiKeyMicroClient._endpoint['delete'],
            apiKeyId='apikey-1',
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert result is True
