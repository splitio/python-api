from __future__ import absolute_import, division, print_function, \
    unicode_literals

import json
from splitapiclient.microclients.harness import TokenMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import Token
from splitapiclient.tests.microclients.harness.conftest import FakeResponse


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
        
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = TokenMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/ng/api/token/aggregate?apiKeyType=SERVICE_ACCOUNT&accountIdentifier={accountIdentifier}&pageIndex={pageIndex}&pageSize=100'
        
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
            accountIdentifier='test_account',
            pageIndex=0
        )
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
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
        tmc.list.assert_called_once_with(account_identifier='test_account', org_identifier=None, project_identifier=None)
        
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = TokenMicroClient._endpoint['create'].copy()
        expected_endpoint['url_template'] = '/ng/api/token?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = TokenMicroClient._endpoint['update_token'].copy()
        expected_endpoint['url_template'] = '/ng/api/token/{tokenId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = TokenMicroClient._endpoint['rotate_token'].copy()
        expected_endpoint['url_template'] = '/ng/api/token/rotate/{tokenId}?accountIdentifier={accountIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}&apiKeyIdentifier={apiKeyIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = TokenMicroClient._endpoint['delete'].copy()
        expected_endpoint['url_template'] = '/ng/api/token/{tokenId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            tokenId='token1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True


class TestTokenURLGeneration:
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
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = TokenMicroClient(hc, 'test_account')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_org_identifier_only(self, mocker):
        """Verify list URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = TokenMicroClient(hc, 'test_account', org_identifier='org1')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_both_identifiers(self, mocker):
        """Verify list URL contains both orgIdentifier and projectIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = TokenMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url

    def test_list_url_with_method_override_identifiers(self, mocker):
        """Verify list URL uses method parameters to override instance defaults"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = TokenMicroClient(hc, 'test_account', org_identifier='default_org', project_identifier='default_proj')
        client.list(org_identifier='override_org', project_identifier='override_proj')

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=override_org' in called_url
        assert 'projectIdentifier=override_proj' in called_url
        assert 'default_org' not in called_url
        assert 'default_proj' not in called_url
