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
            'harness_token': 'test-harness-token',
            'account_identifier': 'test-account-identifier'
        })
        
        # Mock responses for each resource type
        token_response = {
            'data': {
                'content': [{
                    'token': {
                        'identifier': 'token-1',
                        'name': 'Token 1',
                        'validFrom': 1609459200000,
                        'validTo': 1640995200000,
                        'valid': True,
                        'accountIdentifier': 'test-account-identifier',
                        'apiKeyIdentifier': 'apikey-1',
                        'parentIdentifier': 'sa-1',
                        'apiKeyType': 'SERVICE_ACCOUNT'
                    }
                }]
            }
        }
        
        token_detail_response = {
            'data': {
                'token': {
                    'identifier': 'token-1',
                    'name': 'Token 1',
                    'validFrom': 1609459200000,
                    'validTo': 1640995200000,
                    'valid': True,
                    'accountIdentifier': 'test-account-identifier',
                    'apiKeyIdentifier': 'apikey-1',
                    'parentIdentifier': 'sa-1',
                    'apiKeyType': 'SERVICE_ACCOUNT'
                }
            }
        }
        
        apikey_response = {
            'data': [
                {
                    'identifier': 'apikey-1',
                    'name': 'API Key 1',
                    'apiKeyType': 'CLIENT',
                    'accountIdentifier': 'test-account-identifier',
                    'description': 'Test API Key'
                }
            ]
        }
        
        apikey_detail_response = {
            'data': {
                'apiKey': {
                    'identifier': 'apikey-1',
                    'name': 'API Key 1',
                    'apiKeyType': 'CLIENT',
                    'accountIdentifier': 'test-account-identifier',
                    'description': 'Test API Key'
                }
            }
        }
        
        service_account_response = {
            'data': [
                {
                    'identifier': 'sa-1',
                    'name': 'Service Account 1',
                    'email': 'sa1@example.com',
                    'accountIdentifier': 'test-account-identifier',
                    'description': 'Test Service Account'
                }
            ]
        }
        
        service_account_detail_response = {
            'data': {
                'serviceAccount': {
                    'identifier': 'sa-1',
                    'name': 'Service Account 1',
                    'email': 'sa1@example.com',
                    'accountIdentifier': 'test-account-identifier',
                    'description': 'Test Service Account'
                }
            }
        }
        
        user_response = {
            'data': {
                'content': [
                    {
                        'user': {
                            'uuid': 'user-1',
                            'name': 'User 1',
                            'email': 'user1@example.com',
                            'accountIdentifier': 'test-account-identifier'
                        }
                    }
                ]
            }
        }
        
        user_detail_response = {
            'data': {
                'user': {
                    'uuid': 'user-1',
                    'name': 'User 1',
                    'email': 'user1@example.com',
                    'accountIdentifier': 'test-account-identifier'
                }
            }
        }
        
        group_response = {
            'data': {
                'content': [
                    {
                        'identifier': 'group-1',
                        'name': 'Group 1',
                        'accountIdentifier': 'test-account-identifier',
                        'description': 'Test Group'
                    }
                ]
            }
        }
        
        group_detail_response = {
            'data': {
                'identifier': 'group-1',
                'name': 'Group 1',
                'accountIdentifier': 'test-account-identifier',
                'description': 'Test Group'
            }
        }
        
        role_response = {
            'data': {
                'content': [{
                    'role': {
                        'identifier': 'role-1',
                        'name': 'Role 1',
                        'accountIdentifier': 'test-account-identifier',
                        'permissions': ['ff_read_flag', 'ff_create_flag']
                    }
                }]
            }
        }
        
        role_detail_response = {
            'data': {
                'role': {
                    'identifier': 'role-1',
                    'name': 'Role 1',
                    'accountIdentifier': 'test-account-identifier',
                    'permissions': ['ff_read_flag', 'ff_create_flag']
                }
            }
        }
        
        resource_group_response = {
            'data': {
                'content': [{
                    'resourceGroup': {
                        'identifier': 'rg-1',
                        'name': 'Resource Group 1',
                        'accountIdentifier': 'test-account-identifier',
                        'description': 'Test Resource Group'
                    }
                }]
            }
        }
        
        resource_group_detail_response = {
            'data': {
                'resourceGroup': {
                    'identifier': 'rg-1',
                    'name': 'Resource Group 1',
                    'accountIdentifier': 'test-account-identifier',
                    'description': 'Test Resource Group'
                }
            }
        }
        
        role_assignment_response = {
            'data': {
                'content': [{
                    'roleAssignment': {
                        'identifier': 'ra-1',
                        'roleIdentifier': 'role-1',
                        'resourceGroupIdentifier': 'rg-1',
                        'accountIdentifier': 'test-account-identifier',
                        'principal': {
                            'identifier': 'user-1',
                            'type': 'USER'
                        }
                    }
                }]
            }
        }
        
        role_assignment_detail_response = {
            'data': {
                'roleAssignment': {
                    'identifier': 'ra-1',
                    'roleIdentifier': 'role-1',
                    'resourceGroupIdentifier': 'rg-1',
                    'accountIdentifier': 'test-account-identifier',
                    'principal': {
                        'identifier': 'user-1',
                        'type': 'USER'
                    }
                }
            }
        }
        
        project_response = {
            'data': {
                'content': [{
                    'project': {
                        'identifier': 'project-1',
                        'name': 'Project 1',
                        'orgIdentifier': 'org-1',
                        'accountIdentifier': 'test-account-identifier',
                        'description': 'Test Project'
                    }
                }]
            }
        }
        
        project_detail_response = {
            'data': {
                'project': {
                    'identifier': 'project-1',
                    'name': 'Project 1',
                    'orgIdentifier': 'org-1',
                    'accountIdentifier': 'test-account-identifier',
                    'description': 'Test Project'
                }
            }
        }
        
        # Mock make_request function for all HTTP clients
        def mock_make_request(endpoint, body=None, **kwargs):
            url_template = endpoint.get('url_template', '')
            method = endpoint.get('method', '')
            page_index = kwargs.get('pageIndex', 0)
            
            # Debug print to identify which endpoint is causing the infinite loop
            print(f"Mock request: {method} {url_template}, page_index={page_index}")
            
            # Handle pagination - for any page > 0, return empty content
            # This ensures pagination loops will terminate
            if page_index > 0:
                return {'data': {'content': []}}
            
            # First page or non-paginated requests
            if '/ng/api/token/aggregate' in url_template and method == 'GET':
                return token_response
            elif '/ng/api/token/' in url_template and method == 'GET':
                return token_detail_response
            elif '/ng/api/apikey' in url_template and 'aggregate' not in url_template and method == 'GET':
                return apikey_response
            elif '/ng/api/apikey/aggregate' in url_template and method == 'GET':
                return apikey_detail_response
            elif '/ng/api/serviceaccount/aggregate' in url_template and method == 'GET':
                return service_account_response
            elif '/ng/api/serviceaccount' in url_template and 'aggregate' not in url_template and method == 'GET':
                return service_account_response
            elif '/ng/api/serviceAccount/' in url_template and method == 'GET':
                return service_account_detail_response
            elif '/ng/api/user/aggregate' in url_template and method == 'POST':
                return user_response
            elif '/ng/api/user/aggregate/' in url_template and method == 'GET':
                return user_detail_response
            elif '/ng/api/user-groups' in url_template and '{groupIdentifier}' not in url_template and method == 'GET':
                return group_response
            elif '/ng/api/user-groups/{groupIdentifier}' in url_template and method == 'GET':
                return group_detail_response
            elif '/authz/api/roles' in url_template and '{roleId}' not in url_template and method == 'GET':
                return role_response
            elif '/authz/api/roles/{roleId}' in url_template and method == 'GET':
                return role_detail_response
            elif '/authz/api/resourceGroups' in url_template and '{resourceGroupId}' not in url_template and method == 'GET':
                return resource_group_response
            elif '/resourcegroup/api/v2/resourceGroup' in url_template and '{resourceGroupId}' not in url_template and method == 'GET':
                return resource_group_response
            elif '/authz/api/resourceGroups/{resourceGroupId}' in url_template and method == 'GET':
                return resource_group_detail_response
            elif '/resourcegroup/api/v2/resourceGroup/{resourceGroupId}' in url_template and method == 'GET':
                return resource_group_detail_response
            elif '/authz/api/roleAssignments' in url_template and '{roleAssignmentId}' not in url_template and method == 'GET':
                return role_assignment_response
            elif '/authz/api/roleAssignments/{roleAssignmentId}' in url_template and method == 'GET':
                return role_assignment_detail_response
            elif '/ng/api/projects/aggregate' in url_template and method == 'GET':
                return project_response
            elif '/ng/api/projects' in url_template and '{projectIdentifier}' not in url_template and method == 'GET':
                return project_response
            elif '/ng/api/projects/' in url_template and method == 'GET':
                return project_detail_response
            
            return {'data': {}}
        
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
        assert tokens[0].name == 'Token 1'
        assert tokens[0].valid is True
        assert tokens[0].api_key_identifier == 'apikey-1'
        assert tokens[0].parent_identifier == 'sa-1'
        assert tokens[0].api_key_type == 'SERVICE_ACCOUNT'
        
        # Test API key operations
        apikeys = client.harness_apikey.list()
        assert len(apikeys) == 1
        assert isinstance(apikeys[0], HarnessApiKey)
        assert apikeys[0].identifier == 'apikey-1'
        assert apikeys[0].name == 'API Key 1'
        assert apikeys[0].api_key_type == 'CLIENT'
        assert apikeys[0].description == 'Test API Key'
        
        # Test service account operations
        service_accounts = client.service_account.list()
        assert len(service_accounts) == 1
        assert isinstance(service_accounts[0], ServiceAccount)
        assert service_accounts[0].identifier == 'sa-1'
        assert service_accounts[0].name == 'Service Account 1'
        assert service_accounts[0].email == 'sa1@example.com'
        
        # Test user operations
        users = client.harness_user.list()
        assert len(users) == 1
        assert isinstance(users[0], HarnessUser)
        assert users[0].id == 'user-1'
        assert users[0].name == 'User 1'
        assert users[0].email == 'user1@example.com'
        
        # Test group operations
        groups = client.harness_group.list()
        assert len(groups) == 1
        assert isinstance(groups[0], HarnessGroup)
        assert groups[0].identifier == 'group-1'
        assert groups[0].name == 'Group 1'
        
        # Test role operations
        roles = client.role.list()
        assert len(roles) == 1
        assert isinstance(roles[0], Role)
        assert roles[0].identifier == 'role-1'
        assert roles[0].name == 'Role 1'
        assert 'ff_read_flag' in roles[0].permissions
        
        # Test resource group operations
        resource_groups = client.resource_group.list()
        assert len(resource_groups) == 1
        assert isinstance(resource_groups[0], ResourceGroup)
        assert resource_groups[0].identifier == 'rg-1'
        assert resource_groups[0].name == 'Resource Group 1'
        
        # Test role assignment operations
        role_assignments = client.role_assignment.list()
        assert len(role_assignments) == 1
        assert isinstance(role_assignments[0], RoleAssignment)
        assert role_assignments[0].identifier == 'ra-1'
        assert role_assignments[0].role_identifier == 'role-1'
        assert role_assignments[0].resource_group_identifier == 'rg-1'
        assert role_assignments[0].principal.get('identifier') == 'user-1'
        assert role_assignments[0].principal.get('type') == 'USER'
        
        # Test project operations
        projects = client.harness_project.list()
        assert len(projects) == 1
        assert isinstance(projects[0], HarnessProject)
        assert projects[0].identifier == 'project-1'
        assert projects[0].name == 'Project 1'
        assert projects[0].org_identifier == 'org-1'
    
    def test_harness_pagination(self, mocker):
        '''
        Test that the HarnessApiClient can handle pagination correctly
        '''
        # Create a HarnessApiClient with mocked HTTP client
        client = HarnessApiClient({
            'harness_token': 'test-harness-token',
            'apikey': 'test-apikey',
            'base_url': 'test-host',
            'harness_base_url': 'test-harness-host',
            'account_identifier': 'test-account-identifier'
        })
        
        # Mock the HTTP client's make_request method
        mocker.patch.object(client._token_client._http_client, 'make_request')
        
        # Set up mock responses for pagination
        token_response_page1 = {
            'data': {
                'content': [
                    {
                        'token': {
                            'identifier': 'token-1',
                            'name': 'Token 1',
                            'accountIdentifier': 'test-account-identifier',
                            'valid': True,
                            'apiKeyIdentifier': 'apikey-1',
                            'parentIdentifier': 'sa-1',
                            'apiKeyType': 'SERVICE_ACCOUNT'
                        }
                    }
                ]
            }
        }
        
        token_response_page2 = {
            'data': {
                'content': [
                    {
                        'token': {
                            'identifier': 'token-2',
                            'name': 'Token 2',
                            'accountIdentifier': 'test-account-identifier',
                            'valid': True,
                            'apiKeyIdentifier': 'apikey-2',
                            'parentIdentifier': 'sa-2',
                            'apiKeyType': 'SERVICE_ACCOUNT'
                        }
                    }
                ]
            }
        }
        
        empty_response = {
            'data': {
                'content': []
            }
        }
        
        # Configure the mock to return different responses for different pages
        client._token_client._http_client.make_request.side_effect = lambda endpoint, **kwargs: (
            token_response_page1 if kwargs.get('pageIndex') == 0 else
            token_response_page2 if kwargs.get('pageIndex') == 1 else
            empty_response
        )
        
        # Test pagination by listing tokens
        tokens = client.token.list(account_identifier='test-account-identifier')
        
        # Verify that we got tokens from both pages
        assert len(tokens) == 2
        assert tokens[0].identifier == 'token-1'
        assert tokens[1].identifier == 'token-2'
        
        # Verify that the make_request method was called with the correct parameters
        # for each page
        assert client._token_client._http_client.make_request.call_count == 3
        
        # First call should be for page 0
        args, kwargs = client._token_client._http_client.make_request.call_args_list[0]
        assert kwargs.get('pageIndex') == 0
        assert kwargs.get('accountIdentifier') == 'test-account-identifier'
        
        # Second call should be for page 1
        args, kwargs = client._token_client._http_client.make_request.call_args_list[1]
        assert kwargs.get('pageIndex') == 1
        assert kwargs.get('accountIdentifier') == 'test-account-identifier'
        
        # Third call should be for page 2
        args, kwargs = client._token_client._http_client.make_request.call_args_list[2]
        assert kwargs.get('pageIndex') == 2
        assert kwargs.get('accountIdentifier') == 'test-account-identifier'
    
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
        
        # Verify that the HTTP client was initialized correctly for client1
        from splitapiclient.http_clients.harness_client import HarnessHttpClient
        
        # For client1, harness_token should be used for Harness endpoints
        harness_client1_calls = [
            call for call in HarnessHttpClient.__init__.call_args_list 
            if call[0][0] == 'https://app.harness.io/' and call[0][1] == 'test-harness-token'
        ]
        assert len(harness_client1_calls) > 0
        
        # Reset the mock before creating client2
        HarnessHttpClient.__init__.reset_mock()
    
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
        
        # For client2, apikey should be used for Harness endpoints
        harness_client2_calls = [
            call for call in HarnessHttpClient.__init__.call_args_list 
            if call[0][0] == 'https://app.harness.io/' and call[0][1] == 'test-apikey'
        ]
        assert len(harness_client2_calls) > 0
