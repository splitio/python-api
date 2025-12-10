from __future__ import absolute_import, division, print_function, \
    unicode_literals

import json
from splitapiclient.microclients.harness import HarnessProjectMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import HarnessProject
from splitapiclient.tests.microclients.harness.conftest import FakeResponse


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
        
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessProjectMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/ng/api/projects?accountIdentifier={accountIdentifier}&pageIndex={pageIndex}&pageSize=50'
        
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
            pageIndex=0,
            accountIdentifier='test_account'
        )
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier query params removed)
        expected_endpoint = HarnessProjectMicroClient._endpoint['get'].copy()
        expected_endpoint['url_template'] = '/ng/api/projects/{projectIdentifier}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier removed)
        expected_endpoint = HarnessProjectMicroClient._endpoint['create'].copy()
        expected_endpoint['url_template'] = '/ng/api/projects?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier query params removed)
        expected_endpoint = HarnessProjectMicroClient._endpoint['update'].copy()
        expected_endpoint['url_template'] = '/ng/api/projects/{projectIdentifier}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier query params removed)
        expected_endpoint = HarnessProjectMicroClient._endpoint['delete'].copy()
        expected_endpoint['url_template'] = '/ng/api/projects/{projectIdentifier}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            projectIdentifier='project1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True


class TestHarnessProjectURLGeneration:
    """
    Tests that verify actual URL generation by mocking at the requests level.
    These tests ensure that optional orgIdentifier is correctly included or
    excluded from the final URL.
    
    NOTE: The projects endpoint does NOT support projectIdentifier as a query parameter.
    """

    # =========================================================================
    # LIST method URL tests
    # =========================================================================

    def test_list_url_without_org_identifier(self, mocker):
        """Verify list URL doesn't contain orgIdentifier when not set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        # First call returns data, second call returns data to trigger second page, third returns empty
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({
                'data': {'content': [], 'totalPages': 1}
            })),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessProjectMicroClient(hc, 'test_account')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        # Verify projectIdentifier is not in URL (projects endpoint doesn't support it)
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_org_identifier(self, mocker):
        """Verify list URL contains orgIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({
                'data': {'content': [], 'totalPages': 1}
            })),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessProjectMicroClient(hc, 'test_account', org_identifier='org1')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        # Verify projectIdentifier is not in URL
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_method_override_org_identifier(self, mocker):
        """Verify list URL uses method parameters to override instance org_identifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({
                'data': {'content': [], 'totalPages': 1}
            })),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessProjectMicroClient(hc, 'test_account', org_identifier='default_org')
        client.list(org_identifier='override_org')

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=override_org' in called_url
        assert 'default_org' not in called_url

    # =========================================================================
    # GET method URL tests
    # =========================================================================

    def test_get_url_without_org_identifier(self, mocker):
        """Verify get URL doesn't contain orgIdentifier when not set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'project': {'identifier': 'proj1', 'name': 'Project 1', 'description': '', 'orgIdentifier': 'org1', 'color': '', 'modules': []}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessProjectMicroClient(hc, 'test_account')
        client.get('proj1')

        called_url = mock_get.call_args[0][0]
        assert '/projects/proj1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url

    def test_get_url_with_org_identifier(self, mocker):
        """Verify get URL contains orgIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'project': {'identifier': 'proj1', 'name': 'Project 1', 'description': '', 'orgIdentifier': 'org1', 'color': '', 'modules': []}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessProjectMicroClient(hc, 'test_account', org_identifier='org1')
        client.get('proj1')

        called_url = mock_get.call_args[0][0]
        assert '/projects/proj1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url

    def test_get_url_with_method_override_org_identifier(self, mocker):
        """Verify get URL uses method parameters to override instance org_identifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'project': {'identifier': 'proj1', 'name': 'Project 1', 'description': '', 'orgIdentifier': 'override_org', 'color': '', 'modules': []}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessProjectMicroClient(hc, 'test_account', org_identifier='default_org')
        client.get('proj1', org_identifier='override_org')

        called_url = mock_get.call_args[0][0]
        assert '/projects/proj1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=override_org' in called_url
        assert 'default_org' not in called_url
