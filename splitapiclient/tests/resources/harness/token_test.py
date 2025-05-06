from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import Token
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestToken:
    """
    Tests for the Token resource class
    """

    def test_initialization(self):
        """
        Test initialization of a Token object
        """
        # Test with empty data
        token = Token()
        assert token._id is None
        assert token._identifier is None
        assert token._name is None
        
        # Test with data
        token_data = {
            'identifier': 'token1',
            'name': 'Test Token',
            'validFrom': 1234567890,
            'validTo': 1234567899,
            'valid': True,
            'accountIdentifier': 'test_account',
            'projectIdentifier': 'test_project',
            'orgIdentifier': 'test_org',
            'apiKeyIdentifier': 'api_key1',
            'parentIdentifier': 'parent1',
            'apiKeyType': 'USER',
            'description': 'Test token description',
            'tags': {
                'property1': 'value1',
                'property2': 'value2'
            },
            'sshKeyContent': 'ssh-key-content',
            'sshKeyUsage': ['AUTH']
        }
        
        token = Token(token_data)
        
        # Verify all properties were set correctly
        assert token._id == 'token1'
        assert token._identifier == 'token1'
        assert token._name == 'Test Token'
        assert token._valid_from == 1234567890
        assert token._valid_to == 1234567899
        assert token._valid is True
        assert token._account_identifier == 'test_account'
        assert token._project_identifier == 'test_project'
        assert token._org_identifier == 'test_org'
        assert token._api_key_identifier == 'api_key1'
        assert token._parent_identifier == 'parent1'
        assert token._api_key_type == 'USER'
        assert token._description == 'Test token description'
        assert token._tags == {'property1': 'value1', 'property2': 'value2'}
        assert token._ssh_key_content == 'ssh-key-content'
        assert token._ssh_key_usage == ['AUTH']

    def test_getattr(self):
        """
        Test dynamic property access via __getattr__
        """
        token_data = {
            'identifier': 'token1',
            'name': 'Test Token',
            'validFrom': 1234567890,
            'validTo': 1234567899
        }
        
        token = Token(token_data)
        
        # Test accessing properties via camelCase (direct schema field names)
        assert token.identifier == 'token1'
        assert token.name == 'Test Token'
        assert token.validFrom == 1234567890
        assert token.validTo == 1234567899
        
        # Test accessing properties via snake_case
        assert token.valid_from == 1234567890
        assert token.valid_to == 1234567899
        
        # Test accessing non-existent property
        with pytest.raises(AttributeError):
            token.non_existent_property

    def test_export_dict(self):
        """
        Test exporting token data as a dictionary
        """
        token_data = {
            'identifier': 'token1',
            'name': 'Test Token',
            'validFrom': 1234567890,
            'validTo': 1234567899,
            'valid': True,
            'accountIdentifier': 'test_account'
        }
        
        token = Token(token_data)
        exported_data = token.export_dict()
        
        # Verify exported data contains all original fields
        assert exported_data['identifier'] == 'token1'
        assert exported_data['name'] == 'Test Token'
        assert exported_data['validFrom'] == 1234567890
        assert exported_data['validTo'] == 1234567899
        assert exported_data['valid'] is True
        assert exported_data['accountIdentifier'] == 'test_account'
        
        # Verify fields that weren't in the original data are None in the export
        assert 'projectIdentifier' in exported_data
        assert exported_data['projectIdentifier'] is None
