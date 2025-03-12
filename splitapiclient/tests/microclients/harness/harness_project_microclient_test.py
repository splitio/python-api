from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.microclients.harness import HarnessProjectMicroClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient


class TestHarnessProjectMicroClient:
    '''
    Tests for the HarnessProjectMicroClient class' methods
    '''
    
    def test_list(self, mocker):
        '''
        Test that the list method properly returns a list of HarnessProject objects
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        project_client = HarnessProjectMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'items': [
                {
                    'identifier': 'project-1',
                    'name': 'Project 1',
                    'description': 'Description 1',
                    'orgIdentifier': 'org-1'
                },
                {
                    'identifier': 'project-2',
                    'name': 'Project 2',
                    'description': 'Description 2',
                    'orgIdentifier': 'org-1'
                }
            ]
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = project_client.list()
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['all_items'],
            query_params={}
        )
        
        # Verify the result
        assert len(result) == 2
        assert result[0].identifier == 'project-1'
        assert result[0].name == 'Project 1'
        assert result[1].identifier == 'project-2'
        assert result[1].name == 'Project 2'
    
    def test_list_with_filters(self, mocker):
        '''
        Test that the list method properly handles account and org filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        project_client = HarnessProjectMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'items': [
                {
                    'identifier': 'project-1',
                    'name': 'Project 1',
                    'description': 'Description 1',
                    'orgIdentifier': 'org-1',
                    'accountIdentifier': 'account-1'
                }
            ]
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method with filters
        result = project_client.list(account_id='account-1', org_id='org-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['all_items'],
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1'
            }
        )
        
        # Verify the result
        assert len(result) == 1
        assert result[0].identifier == 'project-1'
        assert result[0].org_identifier == 'org-1'
        assert result[0].account_identifier == 'account-1'
    
    def test_get(self, mocker):
        '''
        Test that the get method properly returns a HarnessProject object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        project_client = HarnessProjectMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'identifier': 'project-1',
            'name': 'Project 1',
            'description': 'Description 1',
            'orgIdentifier': 'org-1'
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = project_client.get('project-1')
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['get_project'],
            projectId='project-1',
            query_params={}
        )
        
        # Verify the result
        assert result.identifier == 'project-1'
        assert result.name == 'Project 1'
        assert result.description == 'Description 1'
        assert result.org_identifier == 'org-1'
    
    def test_get_with_filters(self, mocker):
        '''
        Test that the get method properly handles account and org filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        project_client = HarnessProjectMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'identifier': 'project-1',
            'name': 'Project 1',
            'description': 'Description 1',
            'orgIdentifier': 'org-1',
            'accountIdentifier': 'account-1'
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method with filters
        result = project_client.get('project-1', account_id='account-1', org_id='org-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['get_project'],
            projectId='project-1',
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1'
            }
        )
        
        # Verify the result
        assert result.identifier == 'project-1'
        assert result.org_identifier == 'org-1'
        assert result.account_identifier == 'account-1'
    
    def test_create(self, mocker):
        '''
        Test that the create method properly creates and returns a HarnessProject object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        project_client = HarnessProjectMicroClient(http_client)
        
        # Project data to create
        project_data = {
            'identifier': 'new-project',
            'name': 'New Project',
            'description': 'A new project',
            'orgIdentifier': 'org-1'
        }
        
        # Mock response data (usually the same as input but could have additional fields)
        response_data = project_data.copy()
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = project_client.create(project_data)
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['create'],
            body=project_data
        )
        
        # Verify the result
        assert result.identifier == 'new-project'
        assert result.name == 'New Project'
        assert result.description == 'A new project'
        assert result.org_identifier == 'org-1'
    
    def test_update(self, mocker):
        '''
        Test that the update method properly updates and returns a HarnessProject object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        project_client = HarnessProjectMicroClient(http_client)
        
        # Project data to update
        project_data = {
            'name': 'Updated Project',
            'description': 'An updated project',
            'orgIdentifier': 'org-1'
        }
        
        # Mock response data (usually the same as input but with all fields)
        response_data = project_data.copy()
        response_data['identifier'] = 'project-1'
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = project_client.update('project-1', project_data)
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['update'],
            projectId='project-1',
            body=project_data
        )
        
        # Verify the result
        assert result.identifier == 'project-1'
        assert result.name == 'Updated Project'
        assert result.description == 'An updated project'
        assert result.org_identifier == 'org-1'
    
    def test_delete(self, mocker):
        '''
        Test that the delete method properly deletes a project
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        project_client = HarnessProjectMicroClient(http_client)
        
        # Mock response data (usually empty for delete operations)
        HarnessHttpClient.make_request.return_value = None
        
        # Call the method
        result = project_client.delete('project-1')
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['delete'],
            projectId='project-1',
            query_params={}
        )
        
        # Verify the result
        assert result is True
    
    def test_delete_with_filters(self, mocker):
        '''
        Test that the delete method properly handles account and org filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        project_client = HarnessProjectMicroClient(http_client)
        
        # Mock response data (usually empty for delete operations)
        HarnessHttpClient.make_request.return_value = None
        
        # Call the method with filters
        result = project_client.delete('project-1', account_id='account-1', org_id='org-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['delete'],
            projectId='project-1',
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1'
            }
        )
        
        # Verify the result
        assert result is True
