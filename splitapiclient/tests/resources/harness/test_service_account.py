from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import ServiceAccount
from splitapiclient.http_clients.harness_client import HarnessHttpClient


class TestServiceAccount:
    '''
    Tests for the ServiceAccount class' methods
    '''
    def test_constructor(self, mocker):
        '''
        Test that the constructor properly initializes the ServiceAccount object
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'splitapiclient.resources.base_resource.BaseResource.__init__',
            new=mock_init
        )
        
        service_account_data = {
            'identifier': 'sa-123',
            'name': 'Test Service Account',
            'email': 'test@example.com',
            'description': 'A test service account',
            'accountIdentifier': 'account-123',
            'orgIdentifier': 'org-123',
            'projectIdentifier': 'project-123',
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        service_account = ServiceAccount(service_account_data, client)
        
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(service_account, 'sa-123', client)

    def test_getters(self):
        '''
        Test that getters properly return the values from the ServiceAccount object
        '''
        service_account_data = {
            'identifier': 'sa-123',
            'name': 'Test Service Account',
            'email': 'test@example.com',
            'description': 'A test service account',
            'accountIdentifier': 'account-123',
            'orgIdentifier': 'org-123',
            'projectIdentifier': 'project-123',
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        service_account = ServiceAccount(service_account_data)
        
        assert service_account.identifier == 'sa-123'
        assert service_account.name == 'Test Service Account'
        assert service_account.email == 'test@example.com'
        assert service_account.description == 'A test service account'
        assert service_account.account_identifier == 'account-123'
        assert service_account.org_identifier == 'org-123'
        assert service_account.project_identifier == 'project-123'
        assert service_account.tags == {'key1': 'value1', 'key2': 'value2'}

    def test_export_dict(self):
        '''
        Test that export_dict properly returns a dictionary with the ServiceAccount data
        '''
        service_account_data = {
            'identifier': 'sa-123',
            'name': 'Test Service Account',
            'email': 'test@example.com',
            'description': 'A test service account',
            'accountIdentifier': 'account-123',
            'orgIdentifier': 'org-123',
            'projectIdentifier': 'project-123',
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        service_account = ServiceAccount(service_account_data)
        exported_data = service_account.export_dict()
        
        # Verify all fields are properly exported
        for key, value in service_account_data.items():
            assert exported_data.get(key) == value

    def test_missing_attribute(self):
        '''
        Test that accessing a non-existent attribute raises an AttributeError
        '''
        service_account = ServiceAccount({'identifier': 'sa-123'})
        
        with pytest.raises(AttributeError):
            service_account.non_existent_attribute
