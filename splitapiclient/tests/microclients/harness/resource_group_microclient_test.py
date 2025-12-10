from __future__ import absolute_import, division, print_function, \
    unicode_literals

import json
from splitapiclient.microclients.harness import ResourceGroupMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import ResourceGroup
from splitapiclient.tests.microclients.harness.conftest import FakeResponse


class TestResourceGroupMicroClient:

    def test_list(self, mocker):
        '''
        Test listing resource groups
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rgmc = ResourceGroupMicroClient(sc, 'test_account')
        
        # Mock the API response for the first page
        first_page_data = {
            'data': {
                'content': [
                    {
                        'resourceGroup': {
                            'identifier': 'rg1',
                            'name': 'Resource Group 1',
                            'description': 'Test resource group 1',
                            'accountIdentifier': 'test_account',
                            'resourceFilter': {
                                'includeAllResources': False,
                                'resources': [
                                    {'identifier': 'resource1', 'type': 'FEATURE_FLAG'}
                                ]
                            }
                        }
                    },
                    {
                        'resourceGroup': {
                            'identifier': 'rg2',
                            'name': 'Resource Group 2',
                            'description': 'Test resource group 2',
                            'accountIdentifier': 'test_account',
                            'resourceFilter': {
                                'includeAllResources': True,
                                'resources': []
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
        result = rgmc.list()
        
        # Verify the make_request calls
        assert SyncHttpClient.make_request.call_count == 2
        
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = ResourceGroupMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/resourcegroup/api/v2/resourcegroup?accountIdentifier={accountIdentifier}&pageIndex={pageIndex}&pageSize=100'
        
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
        assert isinstance(result[0], ResourceGroup)
        assert isinstance(result[1], ResourceGroup)
        assert result[0]._identifier == 'rg1'
        assert result[1]._identifier == 'rg2'

    def test_get(self, mocker):
        '''
        Test getting a specific resource group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rgmc = ResourceGroupMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': {
                'resourceGroup': {
                    'identifier': 'rg1',
                    'name': 'Resource Group 1',
                    'description': 'Test resource group 1',
                    'accountIdentifier': 'test_account',
                    'resourceFilter': {
                        'includeAllResources': False,
                        'resources': [
                            {'identifier': 'resource1', 'type': 'FEATURE_FLAG'}
                        ]
                    }
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = rgmc.get('rg1')
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = ResourceGroupMicroClient._endpoint['get_resource_group'].copy()
        expected_endpoint['url_template'] = '/resourcegroup/api/v2/resourcegroup/{resourceGroupId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            resourceGroupId='rg1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, ResourceGroup)
        assert result._identifier == 'rg1'
        assert result._name == 'Resource Group 1'
        assert result._description == 'Test resource group 1'

    def test_create(self, mocker):
        '''
        Test creating a resource group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rgmc = ResourceGroupMicroClient(sc, 'test_account')
        
        # Resource group data to create
        rg_data = {
            'name': 'New Resource Group',
            'description': 'Test resource group',
            'accountIdentifier': 'test_account',
            'resourceFilter': {
                'includeAllResources': False,
                'resources': [
                    {'identifier': 'resource1', 'type': 'FEATURE_FLAG'}
                ]
            }
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'resourceGroup': {
                    'identifier': 'new_rg',
                    'name': 'New Resource Group',
                    'description': 'Test resource group',
                    'accountIdentifier': 'test_account',
                    'resourceFilter': {
                        'includeAllResources': False,
                        'resources': [
                            {'identifier': 'resource1', 'type': 'FEATURE_FLAG'}
                        ]
                    }
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = rgmc.create(rg_data)
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = ResourceGroupMicroClient._endpoint['create'].copy()
        expected_endpoint['url_template'] = '/resourcegroup/api/v2/resourcegroup?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            body=rg_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, ResourceGroup)
        assert result._identifier == 'new_rg'
        assert result._name == 'New Resource Group'
        assert result._description == 'Test resource group'

    def test_update(self, mocker):
        '''
        Test updating a resource group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rgmc = ResourceGroupMicroClient(sc, 'test_account')
        
        # Resource group data to update
        update_data = {
            'name': 'Updated Resource Group',
            'description': 'Updated description',
            'resourceFilter': {
                'includeAllResources': True,
                'resources': []
            }
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'resourceGroup': {
                    'identifier': 'rg1',
                    'name': 'Updated Resource Group',
                    'description': 'Updated description',
                    'accountIdentifier': 'test_account',
                    'resourceFilter': {
                        'includeAllResources': True,
                        'resources': []
                    }
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = rgmc.update('rg1', update_data)
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = ResourceGroupMicroClient._endpoint['update'].copy()
        expected_endpoint['url_template'] = '/resourcegroup/api/v2/resourcegroup/{resourceGroupId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            body=update_data,
            resourceGroupId='rg1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, ResourceGroup)
        assert result._identifier == 'rg1'
        assert result._name == 'Updated Resource Group'
        assert result._description == 'Updated description'

    def test_delete(self, mocker):
        '''
        Test deleting a resource group
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rgmc = ResourceGroupMicroClient(sc, 'test_account')
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = {}
        
        # Call the method being tested
        result = rgmc.delete('rg1')
        
        # Verify the make_request call
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = ResourceGroupMicroClient._endpoint['delete'].copy()
        expected_endpoint['url_template'] = '/resourcegroup/api/v2/resourcegroup/{resourceGroupId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            resourceGroupId='rg1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True


class TestResourceGroupURLGeneration:
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
        client = ResourceGroupMicroClient(hc, 'test_account')
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
        client = ResourceGroupMicroClient(hc, 'test_account', org_identifier='org1')
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
        client = ResourceGroupMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
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
        client = ResourceGroupMicroClient(hc, 'test_account', org_identifier='default_org', project_identifier='default_proj')
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
            'data': {'resourceGroup': {'identifier': 'rg1', 'name': 'RG 1', 'description': '', 'resourceFilter': {}}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ResourceGroupMicroClient(hc, 'test_account')
        client.get('rg1')

        called_url = mock_get.call_args[0][0]
        assert '/resourcegroup/' in called_url
        assert 'rg1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_org_identifier_only(self, mocker):
        """Verify get URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'resourceGroup': {'identifier': 'rg1', 'name': 'RG 1', 'description': '', 'resourceFilter': {}}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ResourceGroupMicroClient(hc, 'test_account', org_identifier='org1')
        client.get('rg1')

        called_url = mock_get.call_args[0][0]
        assert '/resourcegroup/' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_both_identifiers(self, mocker):
        """Verify get URL contains both orgIdentifier and projectIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'resourceGroup': {'identifier': 'rg1', 'name': 'RG 1', 'description': '', 'resourceFilter': {}}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ResourceGroupMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.get('rg1')

        called_url = mock_get.call_args[0][0]
        assert '/resourcegroup/' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url
