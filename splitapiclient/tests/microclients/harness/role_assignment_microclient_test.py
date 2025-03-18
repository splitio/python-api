from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients.harness import RoleAssignmentMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources.harness import RoleAssignment


class TestRoleAssignmentMicroClient:

    def test_list(self, mocker):
        '''
        Test listing role assignments
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        ramc = RoleAssignmentMicroClient(sc, 'test_account')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'roleAssignment': {
                            'identifier': 'ra1',
                            'roleIdentifier': 'role1',
                            'resourceGroupIdentifier': 'rg1',
                            'accountIdentifier': 'test_account',
                            'principal': {
                                'identifier': 'user1',
                                'type': 'USER'
                            }
                        }
                    },
                    {
                        'roleAssignment': {
                            'identifier': 'ra2',
                            'roleIdentifier': 'role2',
                            'resourceGroupIdentifier': 'rg2',
                            'accountIdentifier': 'test_account',
                            'principal': {
                                'identifier': 'user2',
                                'type': 'USER'
                            }
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
        result = ramc.list()
        
        # Verify the make_request calls
        assert SyncHttpClient.make_request.call_count == 2
        SyncHttpClient.make_request.assert_any_call(
            RoleAssignmentMicroClient._endpoint['all_items'],
            accountIdentifier='test_account',
            pageIndex=0
        )
        SyncHttpClient.make_request.assert_any_call(
            RoleAssignmentMicroClient._endpoint['all_items'],
            accountIdentifier='test_account',
            pageIndex=1
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], RoleAssignment)
        assert isinstance(result[1], RoleAssignment)
        assert result[0]._identifier == 'ra1'
        assert result[1]._identifier == 'ra2'

    def test_get(self, mocker):
        '''
        Test getting a specific role assignment
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        ramc = RoleAssignmentMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': {
                'roleAssignment': {
                    'identifier': 'ra1',
                    'roleIdentifier': 'role1',
                    'resourceGroupIdentifier': 'rg1',
                    'accountIdentifier': 'test_account',
                    'principal': {
                        'identifier': 'user1',
                        'type': 'USER'
                    }
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = ramc.get('ra1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            RoleAssignmentMicroClient._endpoint['get_role_assignment'],
            roleAssignmentId='ra1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, RoleAssignment)
        assert result._identifier == 'ra1'
        assert result._role_identifier == 'role1'
        assert result._resource_group_identifier == 'rg1'

    def test_create(self, mocker):
        '''
        Test creating a role assignment
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        ramc = RoleAssignmentMicroClient(sc, 'test_account')
        
        # Role assignment data to create
        ra_data = {
            'roleIdentifier': 'role1',
            'resourceGroupIdentifier': 'rg1',
            'accountIdentifier': 'test_account',
            'principal': {
                'identifier': 'user1',
                'type': 'USER'
            }
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'roleAssignment': {
                    'identifier': 'new_ra',
                    'roleIdentifier': 'role1',
                    'resourceGroupIdentifier': 'rg1',
                    'accountIdentifier': 'test_account',
                    'principal': {
                        'identifier': 'user1',
                        'type': 'USER'
                    }
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = ramc.create(ra_data)
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            RoleAssignmentMicroClient._endpoint['create'],
            body=ra_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, RoleAssignment)
        assert result._identifier == 'new_ra'
        assert result._role_identifier == 'role1'
        assert result._resource_group_identifier == 'rg1'

    def test_delete(self, mocker):
        '''
        Test deleting a role assignment
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        ramc = RoleAssignmentMicroClient(sc, 'test_account')
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = {}
        
        # Call the method being tested
        result = ramc.delete('ra1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            RoleAssignmentMicroClient._endpoint['delete'],
            roleAssignmentId='ra1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True
