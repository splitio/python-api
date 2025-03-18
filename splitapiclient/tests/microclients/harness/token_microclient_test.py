from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients.harness import TokenMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources.harness import Token


class TestTokenMicroClient:

    def test_list(self, mocker):
        '''
        Test listing tokens
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        tmc = TokenMicroClient(sc, 'test_account')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'token': {
                            'identifier': 'token1',
                            'name': 'Test Token 1',
                            'validFrom': 1234567890,
                            'validTo': 1234567899,
                            'scheduledExpireTime': 1234567899,
                            'valid': True,
                            'accountIdentifier': 'test_account',
                            'apiKeyIdentifier': 'api_key1',
                            'parentIdentifier': 'parent1',
                            'apiKeyType': 'USER',
                            'description': 'Test token 1',
                            'tags': {}
                        }
                    },
                    {
                        'token': {
                            'identifier': 'token2',
                            'name': 'Test Token 2',
                            'validFrom': 1234567890,
                            'validTo': 1234567899,
                            'scheduledExpireTime': 1234567899,
                            'valid': True,
                            'accountIdentifier': 'test_account',
                            'apiKeyIdentifier': 'api_key2',
                            'parentIdentifier': 'parent2',
                            'apiKeyType': 'USER',
                            'description': 'Test token 2',
                            'tags': {}
                        }
                    }
                ]
            }
        }
        
        # Mock the API response for the second page (empty to end pagination)
        second_page_data = {
            'data': {
                'content': []
            }
        }
        
        # Set up the mock to return different responses for different calls
        SyncHttpClient.make_request.side_effect = [first_page_data, second_page_data]
        
        # Call the method being tested
        result = tmc.list()
        
        # Verify the make_request calls
        assert SyncHttpClient.make_request.call_count == 2
        SyncHttpClient.make_request.assert_any_call(
            TokenMicroClient._endpoint['all_items'],
            accountIdentifier='test_account',
            pageIndex=0
        )
        SyncHttpClient.make_request.assert_any_call(
            TokenMicroClient._endpoint['all_items'],
            accountIdentifier='test_account',
            pageIndex=1
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], Token)
        assert isinstance(result[1], Token)
        assert result[0]._identifier == 'token1'
        assert result[1]._identifier == 'token2'

    def test_get(self, mocker):
        '''
        Test getting a specific token
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        tmc = TokenMicroClient(sc, 'test_account')
        
        # Create mock tokens to be returned by the list method
        token1 = Token({
            'identifier': 'token1',
            'name': 'Test Token 1',
            'validFrom': 1234567890,
            'validTo': 1234567899,
            'scheduledExpireTime': 1234567899,
            'valid': True,
            'accountIdentifier': 'test_account',
            'apiKeyIdentifier': 'api_key1',
            'parentIdentifier': 'parent1',
            'apiKeyType': 'USER',
            'description': 'Test token 1',
            'tags': {}
        }, sc)
        
        token2 = Token({
            'identifier': 'token2',
            'name': 'Test Token 2',
            'validFrom': 1234567890,
            'validTo': 1234567899,
            'scheduledExpireTime': 1234567899,
            'valid': True,
            'accountIdentifier': 'test_account',
            'apiKeyIdentifier': 'api_key2',
            'parentIdentifier': 'parent2',
            'apiKeyType': 'USER',
            'description': 'Test token 2',
            'tags': {}
        }, sc)
        
        # Mock the list method to return our predefined tokens
        mocker.patch.object(tmc, 'list', return_value=[token1, token2])
        
        # Call the method being tested
        result = tmc.get('token2')
        
        # Verify the list method was called with the correct parameters
        tmc.list.assert_called_once_with(account_identifier='test_account')
        
        # Verify the result
        assert isinstance(result, Token)
        assert result._identifier == 'token2'
        assert result._name == 'Test Token 2'

    def test_create(self, mocker):
        '''
        Test creating a token
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        tmc = TokenMicroClient(sc, 'test_account')
        
        # Token data to create
        token_data = {
            'name': 'New Token',
            'description': 'Test token',
            'apiKeyType': 'SERVICE_ACCOUNT',
            'parentIdentifier': 'parent1',
            'apiKeyIdentifier': 'api_key1'
        }
        
        # Mock the API response
        response_data = {
            'data': 'token123abc'
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = tmc.create(token_data)
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            TokenMicroClient._endpoint['create'],
            body=token_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result == 'token123abc'

    def test_update(self, mocker):
        '''
        Test updating a token
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        tmc = TokenMicroClient(sc, 'test_account')
        
        # Token data to update
        update_data = {
            'name': 'Updated Token',
            'description': 'Updated description'
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'identifier': 'token1',
                'name': 'Updated Token',
                'description': 'Updated description',
                'validFrom': 1234567890,
                'validTo': 1234567899,
                'valid': True,
                'accountIdentifier': 'test_account'
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = tmc.update('token1', update_data)
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            TokenMicroClient._endpoint['update_token'],
            body=update_data,
            tokenId='token1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, Token)
        assert result._identifier == 'token1'
        assert result._name == 'Updated Token'
        assert result._description == 'Updated description'

    def test_rotate(self, mocker):
        '''
        Test rotating a token
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        tmc = TokenMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': 'new_token_value_123'
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = tmc.rotate('token1', 'parent1', 'api_key1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            TokenMicroClient._endpoint['rotate_token'],
            tokenId='token1',
            parentIdentifier='parent1',
            apiKeyIdentifier='api_key1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result == 'new_token_value_123'

    def test_delete(self, mocker):
        '''
        Test deleting a token
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        tmc = TokenMicroClient(sc, 'test_account')
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = {}
        
        # Call the method being tested
        result = tmc.delete('token1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            TokenMicroClient._endpoint['delete'],
            tokenId='token1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True
