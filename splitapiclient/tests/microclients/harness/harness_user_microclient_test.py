from __future__ import absolute_import, division, print_function, \
    unicode_literals

import json
from splitapiclient.microclients.harness import HarnessUserMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import HarnessUser, HarnessInvite
from splitapiclient.tests.microclients.harness.conftest import FakeResponse


class TestHarnessUserMicroClient:

    def test_list(self, mocker):
        '''
        Test listing users
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        umc = HarnessUserMicroClient(sc, 'test_account')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'user': {
                            'uuid': 'user1',
                            'name': 'User 1',
                            'email': 'user1@example.com',
                            'accountIdentifier': 'test_account',
                            'status': 'ACTIVE'
                        }
                    },
                    {
                        'user': {
                            'uuid': 'user2',
                            'name': 'User 2',
                            'email': 'user2@example.com',
                            'accountIdentifier': 'test_account',
                            'status': 'ACTIVE'
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
        result = umc.list()
        
        # Verify the make_request calls
        assert SyncHttpClient.make_request.call_count == 2
        
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessUserMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/ng/api/user/aggregate?accountIdentifier={accountIdentifier}&pageIndex={pageIndex}'
        
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
            pageIndex=0,
            accountIdentifier='test_account'
        )
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
            pageIndex=1,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], HarnessUser)
        assert isinstance(result[1], HarnessUser)
        assert result[0]._uuid == 'user1'
        assert result[1]._uuid == 'user2'

    def test_get(self, mocker):
        '''
        Test getting a specific user
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        umc = HarnessUserMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': {
                'user': {
                    'uuid': 'user1',
                    'name': 'User 1',
                    'email': 'user1@example.com',
                    'accountIdentifier': 'test_account',
                    'status': 'ACTIVE'
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = umc.get('user1')
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessUserMicroClient._endpoint['get_user'].copy()
        expected_endpoint['url_template'] = '/ng/api/user/aggregate/{userId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            userId='user1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, HarnessUser)
        assert result._uuid == 'user1'
        assert result._name == 'User 1'
        assert result._email == 'user1@example.com'

    def test_invite(self, mocker):
        '''
        Test inviting a user
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        umc = HarnessUserMicroClient(sc, 'test_account')
        
        # User data for invitation
        user_data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'userGroups': [
                {'identifier': 'group1', 'type': 'USER_GROUP'}
            ]
        }
        
        # Mock the API response
        response_data = {
            'data': True
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = umc.invite(user_data)
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessUserMicroClient._endpoint['invite'].copy()
        expected_endpoint['url_template'] = '/ng/api/user/users?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            body=user_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True

    def test_update(self, mocker):
        '''
        Test updating a user
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        umc = HarnessUserMicroClient(sc, 'test_account')
        
        # User data to update
        update_data = {
            'name': 'Updated User',
            'email': 'updated@example.com'
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'uuid': 'user1',
                'name': 'Updated User',
                'email': 'updated@example.com',
                'accountIdentifier': 'test_account',
                'status': 'ACTIVE'
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = umc.update('user1', update_data)
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessUserMicroClient._endpoint['update'].copy()
        expected_endpoint['url_template'] = '/ng/api/user/{userId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            body=update_data,
            userId='user1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, HarnessUser)
        assert result._uuid == 'user1'
        assert result._name == 'Updated User'
        assert result._email == 'updated@example.com'

    def test_add_user_to_groups(self, mocker):
        '''
        Test adding a user to groups
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        umc = HarnessUserMicroClient(sc, 'test_account')
        
        # Group IDs to add the user to
        group_ids = ['group1', 'group2']
        
        # Mock the API response
        response_data = {}
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = umc.add_user_to_groups('user1', group_ids)
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessUserMicroClient._endpoint['add_user_to_groups'].copy()
        expected_endpoint['url_template'] = '/ng/api/user/add-user-to-groups/{userId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            body={"userGroupIdsToAdd": group_ids},
            userId='user1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True

    def test_delete_pending(self, mocker):
        '''
        Test deleting a pending invite
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        umc = HarnessUserMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {}
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = umc.delete_pending('invite1')
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessUserMicroClient._endpoint['delete_pending'].copy()
        expected_endpoint['url_template'] = '/ng/api/invites/{inviteId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            inviteId='invite1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True

    def test_list_pending(self, mocker):
        '''
        Test listing pending invites
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        umc = HarnessUserMicroClient(sc, 'test_account')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'id': 'invite1',
                        'email': 'pending1@example.com',
                        'accountIdentifier': 'test_account',
                        'approved': True
                    },
                    {
                        'id': 'invite2',
                        'email': 'pending2@example.com',
                        'accountIdentifier': 'test_account',
                        'approved': True
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
        result = umc.list_pending()
        
        # Verify the make_request calls
        assert SyncHttpClient.make_request.call_count == 2
        
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessUserMicroClient._endpoint['list_pending'].copy()
        expected_endpoint['url_template'] = '/ng/api/invites/aggregate?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
            pageIndex=0,
            accountIdentifier='test_account'
        )
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
            pageIndex=1,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], HarnessInvite)
        assert isinstance(result[1], HarnessInvite)
        assert result[0]._id == 'invite1'
        assert result[1]._id == 'invite2'


class TestHarnessUserURLGeneration:
    """
    Tests that verify actual URL generation by mocking at the requests level.
    These tests ensure that optional parameters (orgIdentifier, projectIdentifier)
    are correctly included or excluded from the final URL.
    """

    # =========================================================================
    # LIST method URL tests (Note: user list uses POST, not GET)
    # =========================================================================

    def test_list_url_without_optional_identifiers(self, mocker):
        """Verify list URL doesn't contain orgIdentifier/projectIdentifier when not set"""
        mock_post = mocker.patch('splitapiclient.http_clients.harness_client.requests.post')
        mock_post.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessUserMicroClient(hc, 'test_account')
        client.list()

        called_url = mock_post.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_org_identifier_only(self, mocker):
        """Verify list URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_post = mocker.patch('splitapiclient.http_clients.harness_client.requests.post')
        mock_post.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessUserMicroClient(hc, 'test_account', org_identifier='org1')
        client.list()

        called_url = mock_post.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_both_identifiers(self, mocker):
        """Verify list URL contains both orgIdentifier and projectIdentifier when set"""
        mock_post = mocker.patch('splitapiclient.http_clients.harness_client.requests.post')
        mock_post.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessUserMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.list()

        called_url = mock_post.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url

    def test_list_url_with_method_override_identifiers(self, mocker):
        """Verify list URL uses method parameters to override instance defaults"""
        mock_post = mocker.patch('splitapiclient.http_clients.harness_client.requests.post')
        mock_post.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessUserMicroClient(hc, 'test_account', org_identifier='default_org', project_identifier='default_proj')
        client.list(org_identifier='override_org', project_identifier='override_proj')

        called_url = mock_post.call_args_list[0][0][0]
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
            'data': {'user': {'uuid': 'user1', 'name': 'User 1', 'email': 'user1@test.com', 'status': 'ACTIVE'}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessUserMicroClient(hc, 'test_account')
        client.get('user1')

        called_url = mock_get.call_args[0][0]
        assert '/user/aggregate/user1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_org_identifier_only(self, mocker):
        """Verify get URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'user': {'uuid': 'user1', 'name': 'User 1', 'email': 'user1@test.com', 'status': 'ACTIVE'}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessUserMicroClient(hc, 'test_account', org_identifier='org1')
        client.get('user1')

        called_url = mock_get.call_args[0][0]
        assert '/user/aggregate/user1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_both_identifiers(self, mocker):
        """Verify get URL contains both orgIdentifier and projectIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'user': {'uuid': 'user1', 'name': 'User 1', 'email': 'user1@test.com', 'status': 'ACTIVE'}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessUserMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.get('user1')

        called_url = mock_get.call_args[0][0]
        assert '/user/aggregate/user1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url
