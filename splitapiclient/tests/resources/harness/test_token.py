from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import Token
from splitapiclient.http_clients.harness_client import HarnessHttpClient


class TestToken:
    '''
    Tests for the Token class' methods
    '''
    def test_constructor(self, mocker):
        '''
        Test that the constructor properly initializes the Token object
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'splitapiclient.resources.base_resource.BaseResource.__init__',
            new=mock_init
        )
        
        token_data = {
            'identifier': 'token-123',
            'name': 'Test Token',
            'validFrom': 1615000000000,
            'validTo': 1625000000000,
            'scheduledExpireTime': 1625000000000,
            'valid': True,
            'accountIdentifier': 'account-123',
            'projectIdentifier': 'project-123',
            'orgIdentifier': 'org-123',
            'apiKeyIdentifier': 'apikey-123',
            'parentIdentifier': 'parent-123',
            'apiKeyType': 'USER',
            'description': 'A test token',
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        token = Token(token_data, client)
        
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(token, 'token-123', client)

    def test_getters(self):
        '''
        Test that getters properly return the values from the Token object
        '''
        token_data = {
            'identifier': 'token-123',
            'name': 'Test Token',
            'validFrom': 1615000000000,
            'validTo': 1625000000000,
            'scheduledExpireTime': 1625000000000,
            'valid': True,
            'accountIdentifier': 'account-123',
            'projectIdentifier': 'project-123',
            'orgIdentifier': 'org-123',
            'apiKeyIdentifier': 'apikey-123',
            'parentIdentifier': 'parent-123',
            'apiKeyType': 'USER',
            'description': 'A test token',
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        token = Token(token_data)
        
        assert token.identifier == 'token-123'
        assert token.name == 'Test Token'
        assert token.valid_from == 1615000000000
        assert token.valid_to == 1625000000000
        assert token.scheduled_expire_time == 1625000000000
        assert token.valid is True
        assert token.account_identifier == 'account-123'
        assert token.project_identifier == 'project-123'
        assert token.org_identifier == 'org-123'
        assert token.api_key_identifier == 'apikey-123'
        assert token.parent_identifier == 'parent-123'
        assert token.api_key_type == 'USER'
        assert token.description == 'A test token'
        assert token.tags == {'key1': 'value1', 'key2': 'value2'}

    def test_export_dict(self):
        '''
        Test that export_dict properly returns a dictionary with the Token data
        '''
        token_data = {
            'identifier': 'token-123',
            'name': 'Test Token',
            'validFrom': 1615000000000,
            'validTo': 1625000000000,
            'scheduledExpireTime': 1625000000000,
            'valid': True,
            'accountIdentifier': 'account-123',
            'projectIdentifier': 'project-123',
            'orgIdentifier': 'org-123',
            'apiKeyIdentifier': 'apikey-123',
            'parentIdentifier': 'parent-123',
            'apiKeyType': 'USER',
            'description': 'A test token',
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        token = Token(token_data)
        exported_data = token.export_dict()
        
        # Verify all fields are properly exported
        for key, value in token_data.items():
            assert exported_data.get(key) == value

    def test_missing_attribute(self):
        '''
        Test that accessing a non-existent attribute raises an AttributeError
        '''
        token = Token({'identifier': 'token-123'})
        
        with pytest.raises(AttributeError):
            token.non_existent_attribute
