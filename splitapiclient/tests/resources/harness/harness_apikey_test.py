from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import HarnessApiKey
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestHarnessApiKey:
    """
    Tests for the HarnessApiKey resource class
    """

    def test_initialization(self):
        """
        Test initialization of a HarnessApiKey object
        """
        # Test with empty data
        apikey = HarnessApiKey()
        assert apikey._id is None
        assert apikey._identifier is None
        assert apikey._name is None
        
        # Test with data
        apikey_data = {
            'identifier': 'apikey1',
            'name': 'Test API Key',
            'description': 'Test API key description',
            'value': 'api_key_value_123',
            'apiKeyType': 'SERVICE_ACCOUNT',
            'parentIdentifier': 'parent1',
            'defaultTimeToExpireToken': 3600,
            'accountIdentifier': 'test_account',
            'projectIdentifier': 'test_project',
            'orgIdentifier': 'test_org',
            'governanceMetadata': {'key': 'value'}
        }
        
        apikey = HarnessApiKey(apikey_data)
        
        # Verify all properties were set correctly
        assert apikey._id == 'apikey1'
        assert apikey._identifier == 'apikey1'
        assert apikey._name == 'Test API Key'
        assert apikey._description == 'Test API key description'
        assert apikey._value == 'api_key_value_123'
        assert apikey._api_key_type == 'SERVICE_ACCOUNT'
        assert apikey._parent_identifier == 'parent1'
        assert apikey._default_time_to_expire_token == 3600
        assert apikey._account_identifier == 'test_account'
        assert apikey._project_identifier == 'test_project'
        assert apikey._org_identifier == 'test_org'
        assert apikey._governance_metadata == {'key': 'value'}

    def test_getattr(self):
        """
        Test dynamic property access via __getattr__
        """
        apikey_data = {
            'identifier': 'apikey1',
            'name': 'Test API Key',
            'apiKeyType': 'SERVICE_ACCOUNT',
            'parentIdentifier': 'parent1',
            'accountIdentifier': 'test_account'
        }
        
        apikey = HarnessApiKey(apikey_data)
        
        # Test accessing properties via camelCase (direct schema field names)
        assert apikey.identifier == 'apikey1'
        assert apikey.name == 'Test API Key'
        assert apikey.apiKeyType == 'SERVICE_ACCOUNT'
        assert apikey.parentIdentifier == 'parent1'
        assert apikey.accountIdentifier == 'test_account'
        
        # Test accessing properties via snake_case
        assert apikey.api_key_type == 'SERVICE_ACCOUNT'
        assert apikey.parent_identifier == 'parent1'
        assert apikey.account_identifier == 'test_account'
        
        # Test accessing non-existent property
        with pytest.raises(AttributeError):
            apikey.non_existent_property

    def test_export_dict(self):
        """
        Test exporting API key data as a dictionary
        """
        apikey_data = {
            'identifier': 'apikey1',
            'name': 'Test API Key',
            'description': 'Test API key description',
            'apiKeyType': 'SERVICE_ACCOUNT',
            'parentIdentifier': 'parent1',
            'accountIdentifier': 'test_account'
        }
        
        apikey = HarnessApiKey(apikey_data)
        exported_data = apikey.export_dict()
        
        # Verify exported data contains all original fields
        assert exported_data['identifier'] == 'apikey1'
        assert exported_data['name'] == 'Test API Key'
        assert exported_data['description'] == 'Test API key description'
        assert exported_data['apiKeyType'] == 'SERVICE_ACCOUNT'
        assert exported_data['parentIdentifier'] == 'parent1'
        assert exported_data['accountIdentifier'] == 'test_account'
        
        # Verify fields that weren't in the original data are None in the export
        assert 'value' in exported_data
        assert exported_data['value'] is None
        assert 'projectIdentifier' in exported_data
        assert exported_data['projectIdentifier'] is None
