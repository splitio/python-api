from __future__ import absolute_import, division, print_function, \
    unicode_literals

import json
from splitapiclient.microclients.harness import ServiceAccountMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.resources.harness import ServiceAccount
from splitapiclient.tests.microclients.harness.conftest import FakeResponse


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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = ServiceAccountMicroClient._endpoint['all_items'].copy()
        expected_endpoint['url_template'] = '/ng/api/serviceaccount?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier removed)
        expected_endpoint = ServiceAccountMicroClient._endpoint['item'].copy()
        expected_endpoint['url_template'] = '/ng/api/serviceaccount/aggregate/{serviceAccountId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = ServiceAccountMicroClient._endpoint['create'].copy()
        expected_endpoint['url_template'] = '/ng/api/serviceaccount?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = ServiceAccountMicroClient._endpoint['update'].copy()
        expected_endpoint['url_template'] = '/ng/api/serviceaccount/{serviceAccountId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
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
        # Create expected endpoint with modified URL template (orgIdentifier and projectIdentifier removed)
        expected_endpoint = ServiceAccountMicroClient._endpoint['delete'].copy()
        expected_endpoint['url_template'] = '/ng/api/serviceaccount/{serviceAccountId}?accountIdentifier={accountIdentifier}'
        
        SyncHttpClient.make_request.assert_called_once_with(
            expected_endpoint,
            serviceAccountId='sa1',
            accountIdentifier='test_account'
        )
        
        # Verify the result
        assert result is True


class TestServiceAccountURLGeneration:
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
        mock_get.return_value = FakeResponse(200, json.dumps({'data': []}))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ServiceAccountMicroClient(hc, 'test_account')
        client.list()

        called_url = mock_get.call_args[0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_org_identifier_only(self, mocker):
        """Verify list URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({'data': []}))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ServiceAccountMicroClient(hc, 'test_account', org_identifier='org1')
        client.list()

        called_url = mock_get.call_args[0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url

    def test_list_url_with_project_identifier_only(self, mocker):
        """Verify list URL contains projectIdentifier when set, but not orgIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({'data': []}))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ServiceAccountMicroClient(hc, 'test_account', project_identifier='proj1')
        client.list()

        called_url = mock_get.call_args[0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier=proj1' in called_url

    def test_list_url_with_both_identifiers(self, mocker):
        """Verify list URL contains both orgIdentifier and projectIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({'data': []}))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ServiceAccountMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.list()

        called_url = mock_get.call_args[0][0]
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url

    def test_list_url_with_method_override_identifiers(self, mocker):
        """Verify list URL uses method parameters to override instance defaults"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({'data': []}))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ServiceAccountMicroClient(hc, 'test_account', org_identifier='default_org', project_identifier='default_proj')
        client.list(org_identifier='override_org', project_identifier='override_proj')

        called_url = mock_get.call_args[0][0]
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
            'data': {'serviceAccount': {'identifier': 'sa1', 'name': 'SA1', 'description': '', 'email': '', 'tags': {}}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ServiceAccountMicroClient(hc, 'test_account')
        client.get('sa1')

        called_url = mock_get.call_args[0][0]
        assert '/serviceaccount/aggregate/sa1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_org_identifier_only(self, mocker):
        """Verify get URL contains orgIdentifier when set, but not projectIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'serviceAccount': {'identifier': 'sa1', 'name': 'SA1', 'description': '', 'email': '', 'tags': {}}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ServiceAccountMicroClient(hc, 'test_account', org_identifier='org1')
        client.get('sa1')

        called_url = mock_get.call_args[0][0]
        assert '/serviceaccount/aggregate/sa1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier' not in called_url

    def test_get_url_with_project_identifier_only(self, mocker):
        """Verify get URL contains projectIdentifier when set, but not orgIdentifier"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'serviceAccount': {'identifier': 'sa1', 'name': 'SA1', 'description': '', 'email': '', 'tags': {}}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ServiceAccountMicroClient(hc, 'test_account', project_identifier='proj1')
        client.get('sa1')

        called_url = mock_get.call_args[0][0]
        assert '/serviceaccount/aggregate/sa1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier' not in called_url
        assert 'projectIdentifier=proj1' in called_url

    def test_get_url_with_both_identifiers(self, mocker):
        """Verify get URL contains both orgIdentifier and projectIdentifier when set"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'serviceAccount': {'identifier': 'sa1', 'name': 'SA1', 'description': '', 'email': '', 'tags': {}}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ServiceAccountMicroClient(hc, 'test_account', org_identifier='org1', project_identifier='proj1')
        client.get('sa1')

        called_url = mock_get.call_args[0][0]
        assert '/serviceaccount/aggregate/sa1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=org1' in called_url
        assert 'projectIdentifier=proj1' in called_url

    def test_get_url_with_method_override_identifiers(self, mocker):
        """Verify get URL uses method parameters to override instance defaults"""
        mock_get = mocker.patch('splitapiclient.http_clients.harness_client.requests.get')
        mock_get.return_value = FakeResponse(200, json.dumps({
            'data': {'serviceAccount': {'identifier': 'sa1', 'name': 'SA1', 'description': '', 'email': '', 'tags': {}}}
        }))

        hc = HarnessHttpClient('https://app.harness.io', 'test_token')
        client = ServiceAccountMicroClient(hc, 'test_account', org_identifier='default_org', project_identifier='default_proj')
        client.get('sa1', org_identifier='override_org', project_identifier='override_proj')

        called_url = mock_get.call_args[0][0]
        assert '/serviceaccount/aggregate/sa1' in called_url
        assert 'accountIdentifier=test_account' in called_url
        assert 'orgIdentifier=override_org' in called_url
        assert 'projectIdentifier=override_proj' in called_url
        assert 'default_org' not in called_url
        assert 'default_proj' not in called_url
