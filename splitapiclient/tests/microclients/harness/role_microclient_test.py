from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.microclients.harness import RoleMicroClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import Role


class TestRoleMicroClient:
    '''
    Tests for the RoleMicroClient class' methods
    '''
    
    def test_list(self, mocker):
        '''
        Test that the list method properly returns a list of Role objects
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        role_client = RoleMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'items': [
                {
                    'identifier': 'role-1',
                    'name': 'Role 1',
                    'description': 'Description 1',
                    'accountIdentifier': 'account-1'
                },
                {
                    'identifier': 'role-2',
                    'name': 'Role 2',
                    'description': 'Description 2',
                    'accountIdentifier': 'account-1'
                }
            ]
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = role_client.list()
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['all_items'],
            query_params={}
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], Role)
        assert result[0].identifier == 'role-1'
        assert result[0].name == 'Role 1'
        assert result[1].identifier == 'role-2'
        assert result[1].name == 'Role 2'
    
    def test_list_with_filters(self, mocker):
        '''
        Test that the list method properly handles account, org, and project filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        role_client = RoleMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'items': [
                {
                    'identifier': 'role-1',
                    'name': 'Role 1',
                    'description': 'Description 1',
                    'accountIdentifier': 'account-1',
                    'orgIdentifier': 'org-1',
                    'projectIdentifier': 'project-1'
                }
            ]
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method with filters
        result = role_client.list(account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['all_items'],
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert len(result) == 1
        assert result[0].identifier == 'role-1'
        assert result[0].account_identifier == 'account-1'
        assert result[0].org_identifier == 'org-1'
        assert result[0].project_identifier == 'project-1'
    
    def test_get(self, mocker):
        '''
        Test that the get method properly returns a Role object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        role_client = RoleMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'identifier': 'role-1',
            'name': 'Role 1',
            'description': 'Description 1',
            'accountIdentifier': 'account-1'
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = role_client.get('role-1')
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['get_role'],
            roleId='role-1',
            query_params={}
        )
        
        # Verify the result
        assert isinstance(result, Role)
        assert result.identifier == 'role-1'
        assert result.name == 'Role 1'
        assert result.description == 'Description 1'
        assert result.account_identifier == 'account-1'
    
    def test_get_with_filters(self, mocker):
        '''
        Test that the get method properly handles account, org, and project filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        role_client = RoleMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'identifier': 'role-1',
            'name': 'Role 1',
            'description': 'Description 1',
            'accountIdentifier': 'account-1',
            'orgIdentifier': 'org-1',
            'projectIdentifier': 'project-1'
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method with filters
        result = role_client.get('role-1', account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['get_role'],
            roleId='role-1',
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert result.identifier == 'role-1'
        assert result.account_identifier == 'account-1'
        assert result.org_identifier == 'org-1'
        assert result.project_identifier == 'project-1'
    
    def test_create(self, mocker):
        '''
        Test that the create method properly creates and returns a Role object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        role_client = RoleMicroClient(http_client)
        
        # Role data to create
        role_data = {
            'name': 'New Role',
            'description': 'A new role',
            'accountIdentifier': 'account-1',
            'orgIdentifier': 'org-1',
            'projectIdentifier': 'project-1',
            'permissions': ['read', 'write']
        }
        
        # Mock response data (usually the same as input but with additional fields)
        response_data = role_data.copy()
        response_data['identifier'] = 'role-new'
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = role_client.create(role_data)
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['create'],
            body=role_data
        )
        
        # Verify the result
        assert isinstance(result, Role)
        assert result.identifier == 'role-new'
        assert result.name == 'New Role'
        assert result.description == 'A new role'
        assert result.account_identifier == 'account-1'
        assert result.org_identifier == 'org-1'
        assert result.project_identifier == 'project-1'
        assert result.permissions == ['read', 'write']
    
    def test_update(self, mocker):
        '''
        Test that the update method properly updates and returns a Role object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        role_client = RoleMicroClient(http_client)
        
        # Role data to update
        role_data = {
            'name': 'Updated Role',
            'description': 'An updated role',
            'permissions': ['read', 'write', 'admin']
        }
        
        # Mock response data (usually the same as input but with all fields)
        response_data = role_data.copy()
        response_data['identifier'] = 'role-1'
        response_data['accountIdentifier'] = 'account-1'
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = role_client.update('role-1', role_data)
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['update'],
            roleId='role-1',
            body=role_data,
            query_params={}
        )
        
        # Verify the result
        assert isinstance(result, Role)
        assert result.identifier == 'role-1'
        assert result.name == 'Updated Role'
        assert result.description == 'An updated role'
        assert result.permissions == ['read', 'write', 'admin']
        assert result.account_identifier == 'account-1'
    
    def test_update_with_filters(self, mocker):
        '''
        Test that the update method properly handles account, org, and project filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        role_client = RoleMicroClient(http_client)
        
        # Role data to update
        role_data = {
            'name': 'Updated Role',
            'description': 'An updated role'
        }
        
        # Mock response data
        response_data = role_data.copy()
        response_data['identifier'] = 'role-1'
        response_data['accountIdentifier'] = 'account-1'
        response_data['orgIdentifier'] = 'org-1'
        response_data['projectIdentifier'] = 'project-1'
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method with filters
        result = role_client.update('role-1', role_data, account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['update'],
            roleId='role-1',
            body=role_data,
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert result.identifier == 'role-1'
        assert result.name == 'Updated Role'
        assert result.account_identifier == 'account-1'
        assert result.org_identifier == 'org-1'
        assert result.project_identifier == 'project-1'
    
    def test_delete(self, mocker):
        '''
        Test that the delete method properly deletes a role
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        role_client = RoleMicroClient(http_client)
        
        # Mock response data (usually empty for delete operations)
        HarnessHttpClient.make_request.return_value = None
        
        # Call the method
        result = role_client.delete('role-1')
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['delete'],
            roleId='role-1',
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
        role_client = RoleMicroClient(http_client)
        
        # Mock response data (usually empty for delete operations)
        HarnessHttpClient.make_request.return_value = None
        
        # Call the method with filters
        result = role_client.delete('role-1', account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            RoleMicroClient._endpoint['delete'],
            roleId='role-1',
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert result is True
