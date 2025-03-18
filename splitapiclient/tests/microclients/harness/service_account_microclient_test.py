from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients.harness import ServiceAccountMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources.harness import ServiceAccount


class TestServiceAccountMicroClient:

    def test_list(self, mocker):
        '''
        Test listing service accounts
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        samc = ServiceAccountMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': [
                {
                    'identifier': 'sa1',
                    'name': 'Service Account 1',
                    'description': 'Test service account 1',
                    'accountIdentifier': 'test_account',
                    'email': 'sa1@example.com',
                    'tags': {}
                },
                {
                    'identifier': 'sa2',
                    'name': 'Service Account 2',
                    'description': 'Test service account 2',
                    'accountIdentifier': 'test_account',
                    'email': 'sa2@example.com',
                    'tags': {}
                }
            ]
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = samc.list()
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['all_items'],
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert len(result) == 2
        assert isinstance(result[0], ServiceAccount)
        assert isinstance(result[1], ServiceAccount)
        assert result[0]._identifier == 'sa1'
        assert result[1]._identifier == 'sa2'

    def test_get(self, mocker):
        '''
        Test getting a specific service account
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        samc = ServiceAccountMicroClient(sc, 'test_account')
        
        # Mock the API response
        response_data = {
            'data': {
                'serviceAccount': {
                    'identifier': 'sa1',
                    'name': 'Service Account 1',
                    'description': 'Test service account 1',
                    'accountIdentifier': 'test_account',
                    'email': 'sa1@example.com',
                    'tags': {}
                }
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = samc.get('sa1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['item'],
            serviceAccountId='sa1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, ServiceAccount)
        assert result._identifier == 'sa1'
        assert result._name == 'Service Account 1'
        assert result._description == 'Test service account 1'

    def test_create(self, mocker):
        '''
        Test creating a service account
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        samc = ServiceAccountMicroClient(sc, 'test_account')
        
        # Service account data to create
        sa_data = {
            'name': 'New Service Account',
            'description': 'Test service account',
            'email': 'new_sa@example.com',
            'tags': {}
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'identifier': 'new_sa',
                'name': 'New Service Account',
                'description': 'Test service account',
                'accountIdentifier': 'test_account',
                'email': 'new_sa@example.com',
                'tags': {}
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = samc.create(sa_data)
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['create'],
            body=sa_data,
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, ServiceAccount)
        assert result._identifier == 'new_sa'
        assert result._name == 'New Service Account'
        assert result._description == 'Test service account'

    def test_update(self, mocker):
        '''
        Test updating a service account
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        samc = ServiceAccountMicroClient(sc, 'test_account')
        
        # Service account data to update
        update_data = {
            'name': 'Updated Service Account',
            'description': 'Updated description'
        }
        
        # Mock the API response
        response_data = {
            'data': {
                'identifier': 'sa1',
                'name': 'Updated Service Account',
                'description': 'Updated description',
                'accountIdentifier': 'test_account',
                'email': 'sa1@example.com',
                'tags': {}
            }
        }
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = response_data
        
        # Call the method being tested
        result = samc.update('sa1', update_data)
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['update'],
            body=update_data,
            serviceAccountId='sa1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert isinstance(result, ServiceAccount)
        assert result._identifier == 'sa1'
        assert result._name == 'Updated Service Account'
        assert result._description == 'Updated description'

    def test_delete(self, mocker):
        '''
        Test deleting a service account
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        samc = ServiceAccountMicroClient(sc, 'test_account')
        
        # Set up the mock to return the response
        SyncHttpClient.make_request.return_value = {}
        
        # Call the method being tested
        result = samc.delete('sa1')
        
        # Verify the make_request call
        SyncHttpClient.make_request.assert_called_once_with(
            ServiceAccountMicroClient._endpoint['delete'],
            serviceAccountId='sa1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True
