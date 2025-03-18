from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients.harness import ResourceGroupMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources.harness import ResourceGroup


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
        SyncHttpClient.make_request.assert_any_call(
            ResourceGroupMicroClient._endpoint['all_items'],
            accountIdentifier='test_account',
            pageIndex=0
        )
        SyncHttpClient.make_request.assert_any_call(
            ResourceGroupMicroClient._endpoint['all_items'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            ResourceGroupMicroClient._endpoint['get_resource_group'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            ResourceGroupMicroClient._endpoint['create'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            ResourceGroupMicroClient._endpoint['update'],
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
        SyncHttpClient.make_request.assert_called_once_with(
            ResourceGroupMicroClient._endpoint['delete'],
            resourceGroupId='rg1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True
