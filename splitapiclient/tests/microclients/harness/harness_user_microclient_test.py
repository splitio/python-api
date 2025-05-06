from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients.harness import HarnessUserMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources.harness import HarnessUser, HarnessInvite


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
        SyncHttpClient.make_request.assert_any_call(
            HarnessUserMicroClient._endpoint['all_items'],
            pageIndex=0,
            accountIdentifier='test_account'
        )
        SyncHttpClient.make_request.assert_any_call(
            HarnessUserMicroClient._endpoint['all_items'],
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
            'uuid': 'user1',
            'name': 'User 1',
            'email': 'user1@example.com',
            'accountIdentifier': 'test_account',
            'status': 'ACTIVE'
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = umc.get('user1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessUserMicroClient._endpoint['get_user'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessUserMicroClient._endpoint['invite'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessUserMicroClient._endpoint['update'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessUserMicroClient._endpoint['add_user_to_groups'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessUserMicroClient._endpoint['delete_pending'],
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
        SyncHttpClient.make_request.assert_any_call(
            HarnessUserMicroClient._endpoint['list_pending'],
            pageIndex=0,
            accountIdentifier='test_account'
        )
        SyncHttpClient.make_request.assert_any_call(
            HarnessUserMicroClient._endpoint['list_pending'],
            pageIndex=1,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], HarnessInvite)
        assert isinstance(result[1], HarnessInvite)
        assert result[0]._id == 'invite1'
        assert result[1]._id == 'invite2'
