from __future__ import absolute_import, division, print_function, \
    unicode_literals

import json
from splitapiclient.microclients.harness import RoleAssignmentMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import RoleAssignment
from splitapiclient.tests.microclients.harness.conftest import FakeResponse


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
        
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = RoleAssignmentMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/authz/api/roleassignments?accountIdentifier={accountIdentifier}&pageIndex={pageIndex}&pageSize=100'
        
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
            accountIdentifier='test_account',
            pageIndex=0
        )
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = RoleAssignmentMicroClient._endpoint['get_role_assignment'].copy()
        expected_endpoint['url_template'] = '/authz/api/roleassignments/{roleAssignmentId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = RoleAssignmentMicroClient._endpoint['create'].copy()
        expected_endpoint['url_template'] = '/authz/api/roleassignments?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = RoleAssignmentMicroClient._endpoint['delete'].copy()
        expected_endpoint['url_template'] = '/authz/api/roleassignments/{roleAssignmentId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            roleAssignmentId='ra1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True


class TestRoleAssignmentURLGeneration:
    """
    Tests that verify actual URL generation by mocking at the requests level.
    These tests ensure that optional parameters (orgIdentifier, projectIdentifier)
    are correctly included or excluded from the final URL.
    """

    # =========================================================================
    # LIST method URL tests
    # =========================================================================

    def test_list_url_without_optional_identifiers(self, mocker):
        """Verify list URL doesn't contain orgIdentifier/projectIdentifier when not set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = RoleAssignmentMicroClient(hc, 'test_account')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_org_identifier_only(self, mocker):
        """Verify list URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = RoleAssignmentMicroClient(hc, 'test_account', org_identifier='org1')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_both_identifiers(self, mocker):
        """Verify list URL contains both orgIdentifier and projectIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = RoleAssignmentMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url

    def test_list_url_with_method_override_identifiers(self, mocker):
        """Verify list URL uses method parameters to override instance defaults"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = RoleAssignmentMicroClient(hc, 'test_account', org_identifier='default_org', project_identifier='default_proj')
        client.list(org_identifier='override_org', project_identifier='override_proj')

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=override_org' in called_url
        assert 'projectIdentifier=override_proj' in called_url
        assert 'default_org' not in called_url
        assert 'default_proj' not in called_url

    # =========================================================================
    # GET method URL tests
    # =========================================================================

    def test_get_url_without_optional_identifiers(self, mocker):
        """Verify get URL doesn't contain orgIdentifier/projectIdentifier when not set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'roleAssignment': {'identifier': 'ra1', 'roleIdentifier': 'role1', 'resourceGroupIdentifier': 'rg1', 'principal': {}}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = RoleAssignmentMicroClient(hc, 'test_account')
        client.get('ra1')

        called_url = mock_get.call_args[0][0]
        assert '/roleassignments/ra1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_org_identifier_only(self, mocker):
        """Verify get URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'roleAssignment': {'identifier': 'ra1', 'roleIdentifier': 'role1', 'resourceGroupIdentifier': 'rg1', 'principal': {}}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = RoleAssignmentMicroClient(hc, 'test_account', org_identifier='org1')
        client.get('ra1')

        called_url = mock_get.call_args[0][0]
        assert '/roleassignments/ra1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_both_identifiers(self, mocker):
        """Verify get URL contains both orgIdentifier and projectIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'roleAssignment': {'identifier': 'ra1', 'roleIdentifier': 'role1', 'resourceGroupIdentifier': 'rg1', 'principal': {}}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = RoleAssignmentMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.get('ra1')

        called_url = mock_get.call_args[0][0]
        assert '/roleassignments/ra1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url
