from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients.harness import HarnessProjectMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources.harness import HarnessProject


class TestHarnessProjectMicroClient:

    def test_list(self, mocker):
        '''
        Test listing projects
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        pmc = HarnessProjectMicroClient(sc, 'test_account')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'project': {
                            'identifier': 'project1',
                            'name': 'Project 1',
                            'description': 'Test project 1',
                            'accountIdentifier': 'test_account',
                            'orgIdentifier': 'org1',
                            'color': '#FF0000',
                            'modules': ['FF']
                        }
                    },
                    {
                        'project': {
                            'identifier': 'project2',
                            'name': 'Project 2',
                            'description': 'Test project 2',
                            'accountIdentifier': 'test_account',
                            'orgIdentifier': 'org1',
                            'color': '#00FF00',
                            'modules': ['FF']
                        }
                    }
                ],
                'totalElements': 3,
                'totalPages': 2
            }
        }
        
        # Mock the API response for the second page with one more project
        second_page_data = {
            'data': {
                'content': [
                    {
                        'project': {
                            'identifier': 'project3',
                            'name': 'Project 3',
                            'description': 'Test project 3',
                            'accountIdentifier': 'test_account',
                            'orgIdentifier': 'org1',
                            'color': '#0000FF',
                            'modules': ['FF']
                        }
                    }
                ],
                'totalElements': 3,
                'totalPages': 2
            }
        }
        
        # Set up the mock to return different responses for different calls
        # Note: We only need two responses because the code will stop after page 1 (second page)
        # since totalPages is set to 2 and our pagination is 0-indexed
        SyncHttpClient.make_request.side_effect = [first_page_data, second_page_data]
        
        # Call the method being tested
        result = pmc.list()
        
        # Verify the make_request calls - should only be 2 calls now since we're respecting totalPages
        assert SyncHttpClient.make_request.call_count == 2
        SyncHttpClient.make_request.assert_any_call(
            HarnessProjectMicroClient._endpoint['all_items'],
            pageIndex=0,
            accountIdentifier='test_account'
        )
        SyncHttpClient.make_request.assert_any_call(
            HarnessProjectMicroClient._endpoint['all_items'],
            pageIndex=1,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert len(result) == 3
        assert isinstance(result[0], HarnessProject)
        assert isinstance(result[1], HarnessProject)
        assert isinstance(result[2], HarnessProject)
        assert result[0]._identifier == 'project1'
        assert result[1]._identifier == 'project2'
        assert result[2]._identifier == 'project3'

    def test_get(self, mocker):
        '''
        Test getting a specific project
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        pmc = HarnessProjectMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': {
                'project': {
                    'identifier': 'project1',
                    'name': 'Project 1',
                    'description': 'Test project 1',
                    'accountIdentifier': 'test_account',
                    'orgIdentifier': 'org1',
                    'color': '#FF0000',
                    'modules': ['FF']
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = pmc.get('project1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['get'],
            projectIdentifier='project1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, HarnessProject)
        assert result._identifier == 'project1'
        assert result._name == 'Project 1'
        assert result._description == 'Test project 1'

    def test_create(self, mocker):
        '''
        Test creating a project
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        pmc = HarnessProjectMicroClient(sc, 'test_account')
        
        # Project data to create
        project_data = {
            'name': 'New Project',
            'description': 'Test project',
            'accountIdentifier': 'test_account',
            'orgIdentifier': 'org1',
            'color': '#0000FF',
            'modules': ['FF']
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'project': {
                    'identifier': 'new_project',
                    'name': 'New Project',
                    'description': 'Test project',
                    'accountIdentifier': 'test_account',
                    'orgIdentifier': 'org1',
                    'color': '#0000FF',
                    'modules': ['FF']
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = pmc.create(project_data)
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['create'],
            body=project_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, HarnessProject)
        assert result._identifier == 'new_project'
        assert result._name == 'New Project'
        assert result._description == 'Test project'

    def test_update(self, mocker):
        '''
        Test updating a project
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        pmc = HarnessProjectMicroClient(sc, 'test_account')
        
        # Project data to update
        update_data = {
            'name': 'Updated Project',
            'description': 'Updated description',
            'color': '#FFFF00'
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'project': {
                    'identifier': 'project1',
                    'name': 'Updated Project',
                    'description': 'Updated description',
                    'accountIdentifier': 'test_account',
                    'orgIdentifier': 'org1',
                    'color': '#FFFF00',
                    'modules': ['FF']
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = pmc.update('project1', update_data)
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['update'],
            projectIdentifier='project1',
            accountIdentifier='test_account',
            body=update_data
        )
        
        # Verify the result
        assert isinstance(result, HarnessProject)
        assert result._identifier == 'project1'
        assert result._name == 'Updated Project'
        assert result._description == 'Updated description'

    def test_delete(self, mocker):
        '''
        Test deleting a project
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        pmc = HarnessProjectMicroClient(sc, 'test_account')
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = {}
        
        # Call the method being tested
        result = pmc.delete('project1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            HarnessProjectMicroClient._endpoint['delete'],
            projectIdentifier='project1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True
