from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients.harness import RoleMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources.harness import Role


class TestRoleMicroClient:

    def test_list(self, mocker):
        '''
        Test listing roles
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rmc = RoleMicroClient(sc, 'test_account')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'role': {
                            'identifier': 'role1',
                            'name': 'Role 1',
                            'description': 'Test role 1',
                            'accountIdentifier': 'test_account',
                            'permissions': ['permission1', 'permission2']
                        }
                    },
                    {
                        'role': {
                            'identifier': 'role2',
                            'name': 'Role 2',
                            'description': 'Test role 2',
                            'accountIdentifier': 'test_account',
                            'permissions': ['permission3', 'permission4']
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
        result = rmc.list()
        
        # Verify the make_request calls
        assert SyncHttpClient.make_request.call_count == 2
        SyncHttpClient.make_request.assert_any_call(
            RoleMicroClient._endpoint['all_items'],
            accountIdentifier='test_account',
            pageIndex=0
        )
        SyncHttpClient.make_request.assert_any_call(
            RoleMicroClient._endpoint['all_items'],
            accountIdentifier='test_account',
            pageIndex=1
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], Role)
        assert isinstance(result[1], Role)
        assert result[0]._identifier == 'role1'
        assert result[1]._identifier == 'role2'

    def test_get(self, mocker):
        '''
        Test getting a specific role
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rmc = RoleMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': {
                'role': {
                    'identifier': 'role1',
                    'name': 'Role 1',
                    'description': 'Test role 1',
                    'accountIdentifier': 'test_account',
                    'permissions': ['permission1', 'permission2']
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = rmc.get('role1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['get_role'],
            roleId='role1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, Role)
        assert result._identifier == 'role1'
        assert result._name == 'Role 1'
        assert result._description == 'Test role 1'

    def test_create(self, mocker):
        '''
        Test creating a role
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rmc = RoleMicroClient(sc, 'test_account')
        
        # Role data to create
        role_data = {
            'name': 'New Role',
            'description': 'Test role',
            'accountIdentifier': 'test_account',
            'permissions': ['permission1', 'permission2']
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'role': {
                    'identifier': 'new_role',
                    'name': 'New Role',
                    'description': 'Test role',
                    'accountIdentifier': 'test_account',
                    'permissions': ['permission1', 'permission2']
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = rmc.create(role_data)
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['create'],
            body=role_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, Role)
        assert result._identifier == 'new_role'
        assert result._name == 'New Role'
        assert result._description == 'Test role'

    def test_update(self, mocker):
        '''
        Test updating a role
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rmc = RoleMicroClient(sc, 'test_account')
        
        # Role data to update
        update_data = {
            'name': 'Updated Role',
            'description': 'Updated description',
            'permissions': ['permission1', 'permission2', 'permission3']
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'role': {
                    'identifier': 'role1',
                    'name': 'Updated Role',
                    'description': 'Updated description',
                    'accountIdentifier': 'test_account',
                    'permissions': ['permission1', 'permission2', 'permission3']
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = rmc.update('role1', update_data)
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['update'],
            body=update_data,
            roleId='role1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, Role)
        assert result._identifier == 'role1'
        assert result._name == 'Updated Role'
        assert result._description == 'Updated description'

    def test_delete(self, mocker):
        '''
        Test deleting a role
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rmc = RoleMicroClient(sc, 'test_account')
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = {}
        
        # Call the method being tested
        result = rmc.delete('role1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['delete'],
            roleId='role1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True
