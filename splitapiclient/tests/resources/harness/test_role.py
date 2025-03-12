from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import Role
from splitapiclient.http_clients.harness_client import HarnessHttpClient


class TestRole:
    '''
    Tests for the Role class' methods
    '''
    def test_constructor(self, mocker):
        '''
        Test that the constructor properly initializes the Role object
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'splitapiclient.resources.base_resource.BaseResource.__init__',
            new=mock_init
        )
        
        role_data = {
            'identifier': 'role-123',
            'name': 'Test Role',
            'description': 'A test role',
            'accountIdentifier': 'account-123',
            'orgIdentifier': 'org-123',
            'projectIdentifier': 'project-123',
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            },
            'allowedScopeLevels': ['account', 'org', 'project'],
            'permissions': ['read', 'write']
        }
        
        role = Role(role_data, client)
        
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(role, 'role-123', client)

    def test_getters(self):
        '''
        Test that getters properly return the values from the Role object
        '''
        role_data = {
            'identifier': 'role-123',
            'name': 'Test Role',
            'description': 'A test role',
            'accountIdentifier': 'account-123',
            'orgIdentifier': 'org-123',
            'projectIdentifier': 'project-123',
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            },
            'allowedScopeLevels': ['account', 'org', 'project'],
            'permissions': ['read', 'write']
        }
        
        role = Role(role_data)
        
        assert role.identifier == 'role-123'
        assert role.name == 'Test Role'
        assert role.description == 'A test role'
        assert role.account_identifier == 'account-123'
        assert role.org_identifier == 'org-123'
        assert role.project_identifier == 'project-123'
        assert role.tags == {'key1': 'value1', 'key2': 'value2'}
        assert role.allowed_scope_levels == ['account', 'org', 'project']
        assert role.permissions == ['read', 'write']

    def test_export_dict(self):
        '''
        Test that export_dict properly returns a dictionary with the Role data
        '''
        role_data = {
            'identifier': 'role-123',
            'name': 'Test Role',
            'description': 'A test role',
            'accountIdentifier': 'account-123',
            'orgIdentifier': 'org-123',
            'projectIdentifier': 'project-123',
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            },
            'allowedScopeLevels': ['account', 'org', 'project'],
            'permissions': ['read', 'write']
        }
        
        role = Role(role_data)
        exported_data = role.export_dict()
        
        # Verify all fields are properly exported
        for key, value in role_data.items():
            assert exported_data.get(key) == value

    def test_missing_attribute(self):
        '''
        Test that accessing a non-existent attribute raises an AttributeError
        '''
        role = Role({'identifier': 'role-123'})
        
        with pytest.raises(AttributeError):
            role.non_existent_attribute
