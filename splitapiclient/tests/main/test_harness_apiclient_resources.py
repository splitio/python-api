from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.main.harness_apiclient import HarnessApiClient
from splitapiclient.resources.harness import Token, HarnessApiKey, ServiceAccount, HarnessUser
from splitapiclient.resources.harness import HarnessGroup, Role, ResourceGroup, RoleAssignment, HarnessProject
from splitapiclient.microclients.harness import TokenMicroClient, HarnessApiKeyMicroClient, ServiceAccountMicroClient
from splitapiclient.microclients.harness import HarnessUserMicroClient, HarnessGroupMicroClient, RoleMicroClient
from splitapiclient.microclients.harness import ResourceGroupMicroClient, RoleAssignmentMicroClient, HarnessProjectMicroClient


class TestHarnessApiClientResources:
    '''
    Tests for the HarnessApiClient integration with all Harness resources
    '''
    
    def test_harness_resource_properties(self, mocker):
        '''
        Test that all Harness resource properties return the appropriate microclients
        '''
        # Mock the HTTP client initialization to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        
        # Create a HarnessApiClient with minimal config
        client = HarnessApiClient({
            'apikey': 'test-apikey',
            'harness_token': 'test-harness-token'
        })
        
        # Verify that each harness resource property returns the appropriate microclient
        assert isinstance(client.token, TokenMicroClient)
        assert isinstance(client.harness_apikey, HarnessApiKeyMicroClient)
        assert isinstance(client.service_account, ServiceAccountMicroClient)
        assert isinstance(client.harness_user, HarnessUserMicroClient)
        assert isinstance(client.harness_group, HarnessGroupMicroClient)
        assert isinstance(client.role, RoleMicroClient)
        assert isinstance(client.resource_group, ResourceGroupMicroClient)
        assert isinstance(client.role_assignment, RoleAssignmentMicroClient)
        assert isinstance(client.harness_project, HarnessProjectMicroClient)
    
    def test_harness_resource_operations(self, mocker):
        '''
        Test that the HarnessApiClient can perform operations on all Harness resources
        '''
        # Mock the HTTP client to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        
        # Create a HarnessApiClient with minimal config
        client = HarnessApiClient({
            'apikey': 'test-apikey',
            'harness_token': 'test-harness-token'
        })
        
        # Mock responses for each resource type
        token_response = {
            'identifier': 'token-1',
            'name': 'Token 1'
        }
        
        apikey_response = {
            'identifier': 'apikey-1',
            'name': 'API Key 1',
            'apiKeyType': 'CLIENT'
        }
        
        service_account_response = {
            'identifier': 'sa-1',
            'name': 'Service Account 1',
            'email': 'sa1@example.com'
        }
        
        user_response = {
            'identifier': 'user-1',
            'name': 'User 1',
            'email': 'user1@example.com'
        }
        
        group_response = {
            'identifier': 'group-1',
            'name': 'Group 1'
        }
        
        role_response = {
            'identifier': 'role-1',
            'name': 'Role 1',
            'permissions': ['read']
        }
        
        resource_group_response = {
            'identifier': 'rg-1',
            'name': 'Resource Group 1'
        }
        
        role_assignment_response = {
            'identifier': 'ra-1',
            'roleIdentifier': 'role-1',
            'resourceGroupIdentifier': 'rg-1'
        }
        
        project_response = {
            'identifier': 'project-1',
            'name': 'Project 1',
            'orgIdentifier': 'org-1'
        }
        
        # Set up the mock to return different responses based on the endpoint
        def mock_make_request(endpoint, **kwargs):
            url_template = endpoint['url_template']
            method = endpoint['method']
            
            if url_template == 'tokens' and method == 'GET':
                return {'items': [token_response]}
            elif url_template == 'tokens/{tokenId}' and method == 'GET':
                return token_response
            elif url_template == 'apiKeys' and method == 'GET':
                return {'items': [apikey_response]}
            elif url_template == 'apiKeys/{apiKeyId}' and method == 'GET':
                return apikey_response
            elif url_template == 'serviceAccounts' and method == 'GET':
                return {'items': [service_account_response]}
            elif url_template == 'serviceAccounts/{serviceAccountId}' and method == 'GET':
                return service_account_response
            elif url_template == 'users' and method == 'GET':
                return {'items': [user_response]}
            elif url_template == 'users/{userId}' and method == 'GET':
                return user_response
            elif url_template == 'groups' and method == 'GET':
                return {'items': [group_response]}
            elif url_template == 'groups/{groupId}' and method == 'GET':
                return group_response
            elif url_template == 'roles' and method == 'GET':
                return {'items': [role_response]}
            elif url_template == 'roles/{roleId}' and method == 'GET':
                return role_response
            elif url_template == 'resourceGroups' and method == 'GET':
                return {'items': [resource_group_response]}
            elif url_template == 'resourceGroups/{resourceGroupId}' and method == 'GET':
                return resource_group_response
            elif url_template == 'roleAssignments' and method == 'GET':
                return {'items': [role_assignment_response]}
            elif url_template == 'roleAssignments/{roleAssignmentId}' and method == 'GET':
                return role_assignment_response
            elif url_template == 'projects' and method == 'GET':
                return {'items': [project_response]}
            elif url_template == 'projects/{projectId}' and method == 'GET':
                return project_response
            
            return None
        
        client._token_client._http_client.make_request.side_effect = mock_make_request
        client._harness_apikey_client._http_client.make_request.side_effect = mock_make_request
        client._service_account_client._http_client.make_request.side_effect = mock_make_request
        client._harness_user_client._http_client.make_request.side_effect = mock_make_request
        client._harness_group_client._http_client.make_request.side_effect = mock_make_request
        client._role_client._http_client.make_request.side_effect = mock_make_request
        client._resource_group_client._http_client.make_request.side_effect = mock_make_request
        client._role_assignment_client._http_client.make_request.side_effect = mock_make_request
        client._harness_project_client._http_client.make_request.side_effect = mock_make_request
        
        # Test token operations
        tokens = client.token.list()
        assert len(tokens) == 1
        assert isinstance(tokens[0], Token)
        assert tokens[0].identifier == 'token-1'
        
        token = client.token.get('token-1')
        assert isinstance(token, Token)
        assert token.identifier == 'token-1'
        
        # Test API key operations
        apikeys = client.harness_apikey.list()
        assert len(apikeys) == 1
        assert isinstance(apikeys[0], HarnessApiKey)
        assert apikeys[0].identifier == 'apikey-1'
        
        apikey = client.harness_apikey.get('apikey-1')
        assert isinstance(apikey, HarnessApiKey)
        assert apikey.identifier == 'apikey-1'
        
        # Test service account operations
        service_accounts = client.service_account.list()
        assert len(service_accounts) == 1
        assert isinstance(service_accounts[0], ServiceAccount)
        assert service_accounts[0].identifier == 'sa-1'
        
        service_account = client.service_account.get('sa-1')
        assert isinstance(service_account, ServiceAccount)
        assert service_account.identifier == 'sa-1'
        
        # Test user operations
        users = client.harness_user.list()
        assert len(users) == 1
        assert isinstance(users[0], HarnessUser)
        assert users[0].identifier == 'user-1'
        
        user = client.harness_user.get('user-1')
        assert isinstance(user, HarnessUser)
        assert user.identifier == 'user-1'
        
        # Test group operations
        groups = client.harness_group.list()
        assert len(groups) == 1
        assert isinstance(groups[0], HarnessGroup)
        assert groups[0].identifier == 'group-1'
        
        group = client.harness_group.get('group-1')
        assert isinstance(group, HarnessGroup)
        assert group.identifier == 'group-1'
        
        # Test role operations
        roles = client.role.list()
        assert len(roles) == 1
        assert isinstance(roles[0], Role)
        assert roles[0].identifier == 'role-1'
        
        role = client.role.get('role-1')
        assert isinstance(role, Role)
        assert role.identifier == 'role-1'
        
        # Test resource group operations
        resource_groups = client.resource_group.list()
        assert len(resource_groups) == 1
        assert isinstance(resource_groups[0], ResourceGroup)
        assert resource_groups[0].identifier == 'rg-1'
        
        resource_group = client.resource_group.get('rg-1')
        assert isinstance(resource_group, ResourceGroup)
        assert resource_group.identifier == 'rg-1'
        
        # Test role assignment operations
        role_assignments = client.role_assignment.list()
        assert len(role_assignments) == 1
        assert isinstance(role_assignments[0], RoleAssignment)
        assert role_assignments[0].identifier == 'ra-1'
        
        role_assignment = client.role_assignment.get('ra-1')
        assert isinstance(role_assignment, RoleAssignment)
        assert role_assignment.identifier == 'ra-1'
        
        # Test project operations
        projects = client.harness_project.list()
        assert len(projects) == 1
        assert isinstance(projects[0], HarnessProject)
        assert projects[0].identifier == 'project-1'
        
        project = client.harness_project.get('project-1')
        assert isinstance(project, HarnessProject)
        assert project.identifier == 'project-1'
    
    def test_harness_authentication_modes(self, mocker):
        '''
        Test that the HarnessApiClient properly handles different authentication modes
        '''
        # Mock the HTTP client initialization to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        
        # Test with both apikey and harness_token
        client1 = HarnessApiClient({
            'apikey': 'test-apikey',
            'harness_token': 'test-harness-token'
        })
        
        # Test with only apikey
        client2 = HarnessApiClient({
            'apikey': 'test-apikey'
        })
        
        # Verify that both clients have all the Harness resource properties
        for client in [client1, client2]:
            assert hasattr(client, 'token')
            assert hasattr(client, 'harness_apikey')
            assert hasattr(client, 'service_account')
            assert hasattr(client, 'harness_user')
            assert hasattr(client, 'harness_group')
            assert hasattr(client, 'role')
            assert hasattr(client, 'resource_group')
            assert hasattr(client, 'role_assignment')
            assert hasattr(client, 'harness_project')
        
        # Verify that the HTTP client was initialized correctly
        from splitapiclient.http_clients.harness_client import HarnessHttpClient
        
        # For client1, harness_token should be used for Harness endpoints
        harness_client1_calls = [
            call for call in HarnessHttpClient.__init__.call_args_list 
            if call[0][0] == 'https://app.harness.io/gateway/ff/api/v2' and call[0][1] == 'test-harness-token'
        ]
        assert len(harness_client1_calls) > 0
        
        # For client2, apikey should be used for Harness endpoints
        HarnessHttpClient.__init__.reset_mock()
        harness_client2_calls = [
            call for call in HarnessHttpClient.__init__.call_args_list 
            if call[0][0] == 'https://app.harness.io/gateway/ff/api/v2' and call[0][1] == 'test-apikey'
        ]
        assert len(harness_client2_calls) > 0
