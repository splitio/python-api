from __future__ import absolute_import, division, print_function, \
    unicode_literals

import json
from splitapiclient.microclients.harness import HarnessGroupMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import HarnessGroup
from splitapiclient.tests.microclients.harness.conftest import FakeResponse


class TestHarnessGroupMicroClient:

    def test_list(self, mocker):
        '''
        Test listing groups
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'identifier': 'group1',
                        'name': 'Group 1',
                        'accountIdentifier': 'test_account',
                        'users': []
                    },
                    {
                        'identifier': 'group2',
                        'name': 'Group 2',
                        'accountIdentifier': 'test_account',
                        'users': []
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
        result = gmc.list()
        
        # Verify the make_request calls
        assert SyncHttpClient.make_request.call_count == 2
        
        # Create expected endpoint with modified URL template (orgIdentifier, projectIdentifier, and filterType removed)
        expected_endpoint = HarnessGroupMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/ng/api/user-groups?accountIdentifier={accountIdentifier}&pageIndex={pageIndex}&pageSize=100'
        
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
        assert len(result) == 2
        assert isinstance(result[0], HarnessGroup)
        assert isinstance(result[1], HarnessGroup)
        assert result[0]._identifier == 'group1'
        assert result[1]._identifier == 'group2'

    def test_get(self, mocker):
        '''
        Test getting a specific group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': {
                'identifier': 'group1',
                'name': 'Group 1',
                'accountIdentifier': 'test_account',
                'users': []
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = gmc.get('group1')
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessGroupMicroClient._endpoint['get_group'].copy()
        expected_endpoint['url_template'] = '/ng/api/user-groups/{groupIdentifier}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            groupIdentifier='group1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, HarnessGroup)
        assert result._identifier == 'group1'
        assert result._name == 'Group 1'

    def test_create(self, mocker):
        '''
        Test creating a group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Group data to create
        group_data = {
            'name': 'New Group',
            'description': 'Test group',
            'accountIdentifier': 'test_account',
            'isSSOLinked': False,
            'linkedSSO': None,
            'users': []
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'identifier': 'new_group',
                'name': 'New Group',
                'description': 'Test group',
                'accountIdentifier': 'test_account',
                'isSSOLinked': False,
                'linkedSSO': None,
                'users': []
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = gmc.create(group_data)
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessGroupMicroClient._endpoint['create'].copy()
        expected_endpoint['url_template'] = '/ng/api/user-groups?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            body=group_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, HarnessGroup)
        assert result._identifier == 'new_group'
        assert result._name == 'New Group'
        assert result._description == 'Test group'

    def test_update(self, mocker):
        '''
        Test updating a group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Group data to update
        update_data = {
            'identifier': 'group1',
            'name': 'Updated Group',
            'description': 'Updated description',
            'accountIdentifier': 'test_account'
        }
        
        # Mock the API response
        response_data = {
            'identifier': 'group1',
            'name': 'Updated Group',
            'description': 'Updated description',
            'accountIdentifier': 'test_account',
            'isSSOLinked': False,
            'linkedSSO': None,
            'users': []
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = gmc.update(update_data)
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessGroupMicroClient._endpoint['update'].copy()
        expected_endpoint['url_template'] = '/ng/api/user-groups?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            body=update_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, HarnessGroup)
        assert result._identifier == 'group1'
        assert result._name == 'Updated Group'
        assert result._description == 'Updated description'

    def test_delete(self, mocker):
        '''
        Test deleting a group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = {}
        
        # Call the method being tested
        result = gmc.delete('group1')
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = HarnessGroupMicroClient._endpoint['delete'].copy()
        expected_endpoint['url_template'] = '/ng/api/user-groups/{groupIdentifier}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            groupIdentifier='group1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True

    def test_list_with_filter_type(self, mocker):
        '''
        Test listing groups with filterType parameter
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'identifier': 'group1',
                        'name': 'Group 1',
                        'accountIdentifier': 'test_account',
                        'users': []
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
        
        # Call the method being tested with filterType
        result = gmc.list(filterType='EXCLUDE_INHERITED_GROUPS')
        
        # Verify the make_request calls
        assert SyncHttpClient.make_request.call_count == 2
        
        # Create expected endpoint with filterType included, but orgIdentifier and projectIdentifier removed
        expected_endpoint = HarnessGroupMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/ng/api/user-groups?accountIdentifier={accountIdentifier}&pageIndex={pageIndex}&pageSize=100&filterType={filterType}'
        
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
            pageIndex=0,
            accountIdentifier='test_account',
            filterType='EXCLUDE_INHERITED_GROUPS'
        )
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
            pageIndex=1,
            accountIdentifier='test_account',
            filterType='EXCLUDE_INHERITED_GROUPS'
        )
        
        # Verify the result
        assert len(result) == 1
        assert isinstance(result[0], HarnessGroup)
        assert result[0]._identifier == 'group1'

    def test_list_with_filter_type_and_org_identifier(self, mocker):
        '''
        Test listing groups with filterType and org_identifier parameters
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account', org_identifier='test_org')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'identifier': 'group1',
                        'name': 'Group 1',
                        'accountIdentifier': 'test_account',
                        'users': []
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
        
        # Call the method being tested with filterType
        result = gmc.list(filterType='INCLUDE_INHERITED_GROUPS')
        
        # Verify the make_request calls
        assert SyncHttpClient.make_request.call_count == 2
        
        # Create expected endpoint with filterType and orgIdentifier included, but projectIdentifier removed
        expected_endpoint = HarnessGroupMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/ng/api/user-groups?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&pageIndex={pageIndex}&pageSize=100&filterType={filterType}'
        
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
            pageIndex=0,
            accountIdentifier='test_account',
            orgIdentifier='test_org',
            filterType='INCLUDE_INHERITED_GROUPS'
        )
        
        # Verify the result
        assert len(result) == 1
        assert isinstance(result[0], HarnessGroup)

    def test_list_with_filter_type_none(self, mocker):
        '''
        Test listing groups with filterType=None (should be omitted from URL)
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'identifier': 'group1',
                        'name': 'Group 1',
                        'accountIdentifier': 'test_account',
                        'users': []
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
        
        # Call the method being tested with filterType=None (explicit)
        result = gmc.list(filterType=None)
        
        # Verify the make_request calls
        assert SyncHttpClient.make_request.call_count == 2
        
        # Create expected endpoint with filterType removed (since it's None)
        expected_endpoint = HarnessGroupMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/ng/api/user-groups?accountIdentifier={accountIdentifier}&pageIndex={pageIndex}&pageSize=100'
        
        SyncHttpClient.make_request.assert_any_call(
            expected_endpoint,
            pageIndex=0,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert len(result) == 1
        assert isinstance(result[0], HarnessGroup)


class TestHarnessGroupURLGeneration:
    """
    Tests that verify actual URL generation by mocking at the requests level.
    These tests ensure that optional parameters (orgIdentifier, projectIdentifier, filterType)
    are correctly included or excluded from the final URL.
    """

    # =========================================================================
    # LIST method URL tests
    # =========================================================================

    def test_list_url_without_optional_identifiers(self, mocker):
        """Verify list URL doesn't contain orgIdentifier/projectIdentifier/filterType when not set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        # Return empty content on second call to stop pagination
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessGroupMicroClient(hc, 'test_account')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url
        assert 'filterType' not in called_url

    def test_list_url_with_org_identifier_only(self, mocker):
        """Verify list URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessGroupMicroClient(hc, 'test_account', org_identifier='org1')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url
        assert 'filterType' not in called_url

    def test_list_url_with_project_identifier_only(self, mocker):
        """Verify list URL contains projectIdentifier when set, but not orgIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessGroupMicroClient(hc, 'test_account', project_identifier='proj1')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier=proj1' in called_url
        assert 'filterType' not in called_url

    def test_list_url_with_both_identifiers(self, mocker):
        """Verify list URL contains both orgIdentifier and projectIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessGroupMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.list()

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url

    def test_list_url_with_filter_type(self, mocker):
        """Verify list URL contains filterType when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessGroupMicroClient(hc, 'test_account')
        client.list(filterType='EXCLUDE_INHERITED_GROUPS')

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'filterType=EXCLUDE_INHERITED_GROUPS' in called_url

    def test_list_url_with_all_parameters(self, mocker):
        """Verify list URL contains all parameters when all are set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessGroupMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.list(filterType='INCLUDE_INHERITED_GROUPS')

        called_url = mock_get.call_args_list[0][0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url
        assert 'filterType=INCLUDE_INHERITED_GROUPS' in called_url

    def test_list_url_with_method_override_identifiers(self, mocker):
        """Verify list URL uses method parameters to override instance defaults"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.side_effect = [
            FakeResponse(200, json.dumps({'data': {'content': []}})),
        ]

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessGroupMicroClient(hc, 'test_account', org_identifier='default_org', project_identifier='default_proj')
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
            'data': {'identifier': 'group1', 'name': 'Group 1', 'accountIdentifier': 'test_account', 'users': []}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessGroupMicroClient(hc, 'test_account')
        client.get('group1')

        called_url = mock_get.call_args[0][0]
        assert '/user-groups/group1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_org_identifier_only(self, mocker):
        """Verify get URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'identifier': 'group1', 'name': 'Group 1', 'accountIdentifier': 'test_account', 'users': []}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessGroupMicroClient(hc, 'test_account', org_identifier='org1')
        client.get('group1')

        called_url = mock_get.call_args[0][0]
        assert '/user-groups/group1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_both_identifiers(self, mocker):
        """Verify get URL contains both orgIdentifier and projectIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'identifier': 'group1', 'name': 'Group 1', 'accountIdentifier': 'test_account', 'users': []}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = HarnessGroupMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.get('group1')

        called_url = mock_get.call_args[0][0]
        assert '/user-groups/group1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url
