from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.microclients.harness import ServiceAccountMicroClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import ServiceAccount


class TestServiceAccountMicroClient:
    '''
    Tests for the ServiceAccountMicroClient class' methods
    '''
    
    def test_list(self, mocker):
        '''
        Test that the list method properly returns a list of ServiceAccount objects
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        sa_client = ServiceAccountMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'items': [
                {
                    'identifier': 'sa-1',
                    'name': 'Service Account 1',
                    'email': 'sa1@example.com',
                    'accountIdentifier': 'account-1'
                },
                {
                    'identifier': 'sa-2',
                    'name': 'Service Account 2',
                    'email': 'sa2@example.com',
                    'accountIdentifier': 'account-1'
                }
            ]
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = sa_client.list()
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['all_items'],
            query_params={}
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], ServiceAccount)
        assert result[0].identifier == 'sa-1'
        assert result[0].name == 'Service Account 1'
        assert result[1].identifier == 'sa-2'
        assert result[1].name == 'Service Account 2'
    
    def test_list_with_filters(self, mocker):
        '''
        Test that the list method properly handles account, org, and project filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        sa_client = ServiceAccountMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'items': [
                {
                    'identifier': 'sa-1',
                    'name': 'Service Account 1',
                    'email': 'sa1@example.com',
                    'accountIdentifier': 'account-1',
                    'orgIdentifier': 'org-1',
                    'projectIdentifier': 'project-1'
                }
            ]
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method with filters
        result = sa_client.list(account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['all_items'],
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert len(result) == 1
        assert result[0].identifier == 'sa-1'
        assert result[0].account_identifier == 'account-1'
        assert result[0].org_identifier == 'org-1'
        assert result[0].project_identifier == 'project-1'
    
    def test_get(self, mocker):
        '''
        Test that the get method properly returns a ServiceAccount object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        sa_client = ServiceAccountMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'identifier': 'sa-1',
            'name': 'Service Account 1',
            'email': 'sa1@example.com',
            'accountIdentifier': 'account-1'
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = sa_client.get('sa-1')
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['get_service_account'],
            serviceAccountId='sa-1',
            query_params={}
        )
        
        # Verify the result
        assert isinstance(result, ServiceAccount)
        assert result.identifier == 'sa-1'
        assert result.name == 'Service Account 1'
        assert result.email == 'sa1@example.com'
        assert result.account_identifier == 'account-1'
    
    def test_get_with_filters(self, mocker):
        '''
        Test that the get method properly handles account, org, and project filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        sa_client = ServiceAccountMicroClient(http_client)
        
        # Mock response data
        response_data = {
            'identifier': 'sa-1',
            'name': 'Service Account 1',
            'email': 'sa1@example.com',
            'accountIdentifier': 'account-1',
            'orgIdentifier': 'org-1',
            'projectIdentifier': 'project-1'
        }
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method with filters
        result = sa_client.get('sa-1', account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['get_service_account'],
            serviceAccountId='sa-1',
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert result.identifier == 'sa-1'
        assert result.account_identifier == 'account-1'
        assert result.org_identifier == 'org-1'
        assert result.project_identifier == 'project-1'
    
    def test_create(self, mocker):
        '''
        Test that the create method properly creates and returns a ServiceAccount object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        sa_client = ServiceAccountMicroClient(http_client)
        
        # Service Account data to create
        sa_data = {
            'name': 'New Service Account',
            'email': 'new-sa@example.com',
            'description': 'A new service account',
            'accountIdentifier': 'account-1',
            'orgIdentifier': 'org-1',
            'projectIdentifier': 'project-1'
        }
        
        # Mock response data (usually the same as input but with additional fields)
        response_data = sa_data.copy()
        response_data['identifier'] = 'sa-new'
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = sa_client.create(sa_data)
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['create'],
            body=sa_data
        )
        
        # Verify the result
        assert isinstance(result, ServiceAccount)
        assert result.identifier == 'sa-new'
        assert result.name == 'New Service Account'
        assert result.email == 'new-sa@example.com'
        assert result.description == 'A new service account'
        assert result.account_identifier == 'account-1'
        assert result.org_identifier == 'org-1'
        assert result.project_identifier == 'project-1'
    
    def test_update(self, mocker):
        '''
        Test that the update method properly updates and returns a ServiceAccount object
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        sa_client = ServiceAccountMicroClient(http_client)
        
        # Service Account data to update
        sa_data = {
            'name': 'Updated Service Account',
            'description': 'An updated service account'
        }
        
        # Mock response data (usually the same as input but with all fields)
        response_data = sa_data.copy()
        response_data['identifier'] = 'sa-1'
        response_data['email'] = 'sa1@example.com'
        response_data['accountIdentifier'] = 'account-1'
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method
        result = sa_client.update('sa-1', sa_data)
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['update'],
            serviceAccountId='sa-1',
            body=sa_data,
            query_params={}
        )
        
        # Verify the result
        assert isinstance(result, ServiceAccount)
        assert result.identifier == 'sa-1'
        assert result.name == 'Updated Service Account'
        assert result.description == 'An updated service account'
        assert result.email == 'sa1@example.com'
        assert result.account_identifier == 'account-1'
    
    def test_update_with_filters(self, mocker):
        '''
        Test that the update method properly handles account, org, and project filters
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        sa_client = ServiceAccountMicroClient(http_client)
        
        # Service Account data to update
        sa_data = {
            'name': 'Updated Service Account',
            'description': 'An updated service account'
        }
        
        # Mock response data
        response_data = sa_data.copy()
        response_data['identifier'] = 'sa-1'
        response_data['email'] = 'sa1@example.com'
        response_data['accountIdentifier'] = 'account-1'
        response_data['orgIdentifier'] = 'org-1'
        response_data['projectIdentifier'] = 'project-1'
        
        HarnessHttpClient.make_request.return_value = response_data
        
        # Call the method with filters
        result = sa_client.update('sa-1', sa_data, account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['update'],
            serviceAccountId='sa-1',
            body=sa_data,
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert result.identifier == 'sa-1'
        assert result.name == 'Updated Service Account'
        assert result.account_identifier == 'account-1'
        assert result.org_identifier == 'org-1'
        assert result.project_identifier == 'project-1'
    
    def test_delete(self, mocker):
        '''
        Test that the delete method properly deletes a service account
        '''
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        http_client = HarnessHttpClient('https://app.harness.io/gateway/ff/api/v2', 'test-token')
        sa_client = ServiceAccountMicroClient(http_client)
        
        # Mock response data (usually empty for delete operations)
        HarnessHttpClient.make_request.return_value = None
        
        # Call the method
        result = sa_client.delete('sa-1')
        
        # Verify the HTTP request was made correctly
        HarnessHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['delete'],
            serviceAccountId='sa-1',
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
        sa_client = ServiceAccountMicroClient(http_client)
        
        # Mock response data (usually empty for delete operations)
        HarnessHttpClient.make_request.return_value = None
        
        # Call the method with filters
        result = sa_client.delete('sa-1', account_id='account-1', org_id='org-1', project_id='project-1')
        
        # Verify the HTTP request was made correctly with query parameters
        HarnessHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['delete'],
            serviceAccountId='sa-1',
            query_params={
                'accountIdentifier': 'account-1',
                'orgIdentifier': 'org-1',
                'projectIdentifier': 'project-1'
            }
        )
        
        # Verify the result
        assert result is True
