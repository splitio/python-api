from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients.harness import HarnessGroupMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources.harness import HarnessGroup


class TestHarnessGroupMicroClient:

    def test_list(self, mocker):
        '''
        Test listing groups
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'identifier': 'group1',
                        'name': 'Group 1',
                        'accountIdentifier': 'test_account',
                        'users': []
                    },
                    {
                        'identifier': 'group2',
                        'name': 'Group 2',
                        'accountIdentifier': 'test_account',
                        'users': []
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
        result = gmc.list()
        
        # Verify the make_request calls
        assert SyncHttpClient.make_request.call_count == 2
        SyncHttpClient.make_request.assert_any_call(
            HarnessGroupMicroClient._endpoint['all_items'],
            pageIndex=0,
            accountIdentifier='test_account'
        )
        SyncHttpClient.make_request.assert_any_call(
            HarnessGroupMicroClient._endpoint['all_items'],
            pageIndex=1,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], HarnessGroup)
        assert isinstance(result[1], HarnessGroup)
        assert result[0]._identifier == 'group1'
        assert result[1]._identifier == 'group2'

    def test_get(self, mocker):
        '''
        Test getting a specific group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'identifier': 'group1',
            'name': 'Group 1',
            'accountIdentifier': 'test_account',
            'users': []
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = gmc.get('group1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessGroupMicroClient._endpoint['get_group'],
            groupIdentifier='group1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, HarnessGroup)
        assert result._identifier == 'group1'
        assert result._name == 'Group 1'

    def test_create(self, mocker):
        '''
        Test creating a group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Group data to create
        group_data = {
            'name': 'New Group',
            'description': 'Test group',
            'accountIdentifier': 'test_account',
            'isSSOLinked': False,
            'linkedSSO': None,
            'users': []
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'identifier': 'new_group',
                'name': 'New Group',
                'description': 'Test group',
                'accountIdentifier': 'test_account',
                'isSSOLinked': False,
                'linkedSSO': None,
                'users': []
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = gmc.create(group_data)
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessGroupMicroClient._endpoint['create'],
            body=group_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, HarnessGroup)
        assert result._identifier == 'new_group'
        assert result._name == 'New Group'
        assert result._description == 'Test group'

    def test_update(self, mocker):
        '''
        Test updating a group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Group data to update
        update_data = {
            'identifier': 'group1',
            'name': 'Updated Group',
            'description': 'Updated description',
            'accountIdentifier': 'test_account'
        }
        
        # Mock the API response
        response_data = {
            'identifier': 'group1',
            'name': 'Updated Group',
            'description': 'Updated description',
            'accountIdentifier': 'test_account',
            'isSSOLinked': False,
            'linkedSSO': None,
            'users': []
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = gmc.update(update_data)
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessGroupMicroClient._endpoint['update'],
            body=update_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, HarnessGroup)
        assert result._identifier == 'group1'
        assert result._name == 'Updated Group'
        assert result._description == 'Updated description'

    def test_delete(self, mocker):
        '''
        Test deleting a group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = {}
        
        # Call the method being tested
        result = gmc.delete('group1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessGroupMicroClient._endpoint['delete'],
            groupIdentifier='group1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True
