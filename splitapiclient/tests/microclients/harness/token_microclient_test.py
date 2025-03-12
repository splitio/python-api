from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.microclients.harness import TokenMicroClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import Token


class TestTokenMicroClient:
    '''
    Tests for the TokenMicroClient class' methods
    '''
    
    def test_list(self, mocker):
        '''
        Test that the list method properly returns a list of Token objects
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        token_client = TokenMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'items': [
                {
                    'identifier': 'token-1',
                    'name': 'Token 1',
                    'valid': True,
                    'accountIdentifier': 'account-1'
                },
                {
                    'identifier': 'token-2',
                    'name': 'Token 2',
                    'valid': True,
                    'accountIdentifier': 'account-1'
                }
            ]
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = token_client.list()
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            TokenMicroClient._endpoint['all_items']
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], Token)
        assert result[0].identifier == 'token-1'
        assert result[0].name == 'Token 1'
        assert result[1].identifier == 'token-2'
        assert result[1].name == 'Token 2'
    
    def test_get(self, mocker):
        '''
        Test that the get method properly returns a Token object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        token_client = TokenMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'identifier': 'token-1',
            'name': 'Token 1',
            'valid': True,
            'accountIdentifier': 'account-1'
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = token_client.get('token-1')
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            TokenMicroClient._endpoint['get_token'],
            tokenId='token-1'
        )
        
        # Verify the result
        assert isinstance(result, Token)
        assert result.identifier == 'token-1'
        assert result.name == 'Token 1'
        assert result.valid is True
        assert result.account_identifier == 'account-1'
    
    def test_create(self, mocker):
        '''
        Test that the create method properly creates and returns a Token object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        token_client = TokenMicroClient(http_client)
        
        # Token data to create
        token_data = {
            'name': 'New Token',
            'description': 'A new token',
            'accountIdentifier': 'account-1'
        }
        
        # Mock response data (usually the same as input but with additional fields)
        response_data = token_data.copy()
        response_data['identifier'] = 'token-new'
        response_data['valid'] = True
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = token_client.create(token_data)
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            TokenMicroClient._endpoint['create'],
            body=token_data
        )
        
        # Verify the result
        assert isinstance(result, Token)
        assert result.identifier == 'token-new'
        assert result.name == 'New Token'
        assert result.description == 'A new token'
        assert result.account_identifier == 'account-1'
        assert result.valid is True
    
    def test_delete(self, mocker):
        '''
        Test that the delete method properly deletes a token
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        token_client = TokenMicroClient(http_client)
        
        # Mock response data (usually empty for delete operations)
        HarnessHttpClient.make_request.return_value = None
        
        # Call the method
        result = token_client.delete('token-1')
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            TokenMicroClient._endpoint['delete'],
            tokenId='token-1'
        )
        
        # Verify the result
        assert result is True
