from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.main.harness_apiclient import HarnessApiClient
from splitapiclient.resources.harness import HarnessProject
from splitapiclient.microclients.harness import HarnessProjectMicroClient


class TestHarnessApiClientProject:
    '''
    Tests for the HarnessApiClient integration with HarnessProject
    '''
    
    def test_harness_project_property(self, mocker):
        '''
        Test that the harness_project property returns the HarnessProjectMicroClient
        '''
        # Mock the HTTP client initialization to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        
        # Create a HarnessApiClient with minimal config
        client = HarnessApiClient({
            'apikey': 'test-apikey',
            'harness_token': 'test-harness-token'
        })
        
        # Verify that the harness_project property returns a HarnessProjectMicroClient
        assert isinstance(client.harness_project, HarnessProjectMicroClient)
    
    def test_harness_project_operations(self, mocker):
        '''
        Test that the HarnessApiClient can perform operations on HarnessProject resources
        '''
        # Mock the HTTP client to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.make_request')
        
        # Create a HarnessApiClient with minimal config
        client = HarnessApiClient({
            'apikey': 'test-apikey',
            'harness_token': 'test-harness-token'
        })
        
        # Mock response for list operation
        list_response = {
            'items': [
                {
                    'identifier': 'project-1',
                    'name': 'Project 1',
                    'orgIdentifier': 'org-1'
                }
            ]
        }
        
        # Mock response for get operation
        get_response = {
            'identifier': 'project-1',
            'name': 'Project 1',
            'orgIdentifier': 'org-1'
        }
        
        # Set up the mock to return different responses based on the endpoint
        def mock_make_request(endpoint, **kwargs):
            if endpoint['url_template'] == 'projects' and endpoint['method'] == 'GET':
                return list_response
            elif endpoint['url_template'] == 'projects/{projectId}' and endpoint['method'] == 'GET':
                return get_response
            return None
        
        client._harness_project_client._http_client.make_request.side_effect = mock_make_request
        
        # Test list operation
        projects = client.harness_project.list()
        assert len(projects) == 1
        assert isinstance(projects[0], HarnessProject)
        assert projects[0].identifier == 'project-1'
        
        # Test get operation
        project = client.harness_project.get('project-1')
        assert isinstance(project, HarnessProject)
        assert project.identifier == 'project-1'
        assert project.name == 'Project 1'
    
    def test_harness_project_with_apikey_only(self, mocker):
        '''
        Test that the HarnessApiClient can use apikey for Harness endpoints when harness_token is not provided
        '''
        # Mock the HTTP client initialization to avoid actual HTTP requests
        mocker.patch('splitapiclient.http_clients.harness_client.HarnessHttpClient.__init__', return_value=None)
        
        # Create a HarnessApiClient with only apikey (no harness_token)
        client = HarnessApiClient({
            'apikey': 'test-apikey'
        })
        
        # Verify that the harness_project property returns a HarnessProjectMicroClient
        assert isinstance(client.harness_project, HarnessProjectMicroClient)
        
        # Verify that the HTTP client was initialized with the apikey
        from splitapiclient.http_clients.harness_client import HarnessHttpClient
        
        # The last call should be for the Harness HTTP client with the apikey
        # Note: There are multiple calls to HarnessHttpClient.__init__ in the HarnessApiClient constructor
        harness_client_calls = [
            call for call in HarnessHttpClient.__init__.call_args_list 
            if call[0][0] == 'https://app.harness.io/gateway/ff/api/v2'
        ]
        
        # Verify that at least one call was made with the apikey
        assert len(harness_client_calls) > 0
        # The second argument should be the auth token (apikey in this case)
        assert harness_client_calls[-1][0][1] == 'test-apikey'
