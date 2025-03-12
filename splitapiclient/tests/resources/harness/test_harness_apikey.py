from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import HarnessApiKey
from splitapiclient.http_clients.harness_client import HarnessHttpClient


class TestHarnessApiKey:
    '''
    Tests for the HarnessApiKey class' methods
    '''
    def test_constructor(self, mocker):
        '''
        Test that the constructor properly initializes the HarnessApiKey object
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'splitapiclient.resources.base_resource.BaseResource.__init__',
            new=mock_init
        )
        
        apikey_data = {
            'identifier': 'apikey-123',
            'name': 'Test API Key',
            'description': 'A test API key',
            'accountIdentifier': 'account-123',
            'orgIdentifier': 'org-123',
            'projectIdentifier': 'project-123',
            'apiKeyType': 'CLIENT',
            'parentIdentifier': 'parent-123',
            'createdAt': 1615000000000,
            'lastModifiedAt': 1615000000000,
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        apikey = HarnessApiKey(apikey_data, client)
        
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(apikey, 'apikey-123', client)

    def test_getters(self):
        '''
        Test that getters properly return the values from the HarnessApiKey object
        '''
        apikey_data = {
            'identifier': 'apikey-123',
            'name': 'Test API Key',
            'description': 'A test API key',
            'accountIdentifier': 'account-123',
            'orgIdentifier': 'org-123',
            'projectIdentifier': 'project-123',
            'apiKeyType': 'CLIENT',
            'parentIdentifier': 'parent-123',
            'createdAt': 1615000000000,
            'lastModifiedAt': 1615000000000,
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        apikey = HarnessApiKey(apikey_data)
        
        assert apikey.identifier == 'apikey-123'
        assert apikey.name == 'Test API Key'
        assert apikey.description == 'A test API key'
        assert apikey.account_identifier == 'account-123'
        assert apikey.org_identifier == 'org-123'
        assert apikey.project_identifier == 'project-123'
        assert apikey.api_key_type == 'CLIENT'
        assert apikey.parent_identifier == 'parent-123'
        assert apikey.created_at == 1615000000000
        assert apikey.last_modified_at == 1615000000000
        assert apikey.tags == {'key1': 'value1', 'key2': 'value2'}

    def test_export_dict(self):
        '''
        Test that export_dict properly returns a dictionary with the HarnessApiKey data
        '''
        apikey_data = {
            'identifier': 'apikey-123',
            'name': 'Test API Key',
            'description': 'A test API key',
            'accountIdentifier': 'account-123',
            'orgIdentifier': 'org-123',
            'projectIdentifier': 'project-123',
            'apiKeyType': 'CLIENT',
            'parentIdentifier': 'parent-123',
            'createdAt': 1615000000000,
            'lastModifiedAt': 1615000000000,
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        apikey = HarnessApiKey(apikey_data)
        exported_data = apikey.export_dict()
        
        # Verify all fields are properly exported
        for key, value in apikey_data.items():
            assert exported_data.get(key) == value

    def test_missing_attribute(self):
        '''
        Test that accessing a non-existent attribute raises an AttributeError
        '''
        apikey = HarnessApiKey({'identifier': 'apikey-123'})
        
        with pytest.raises(AttributeError):
            apikey.non_existent_attribute
