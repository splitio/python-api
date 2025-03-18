from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import Role
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestRole:
    """
    Tests for the Role resource class
    """

    def test_initialization(self):
        """
        Test initialization of a Role object
        """
        # Test with empty data
        role = Role()
        assert role._id is None
        assert role._identifier is None
        assert role._name is None
        
        # Test with data
        role_data = {
            'identifier': 'role1',
            'name': 'Test Role',
            'description': 'Test role description',
            'permissions': ['permission1', 'permission2', 'permission3'],
            'allowed_scope_levels': ['account', 'project']
        }
        
        role = Role(role_data)
        
        # Verify all properties were set correctly
        assert role._id == 'role1'
        assert role._identifier == 'role1'
        assert role._name == 'Test Role'
        assert role._description == 'Test role description'
        assert role._permissions == ['permission1', 'permission2', 'permission3']
        assert role._allowed_scope_levels == ['account', 'project']

    def test_getattr(self):
        """
        Test dynamic property access via __getattr__
        """
        role_data = {
            'identifier': 'role1',
            'name': 'Test Role',
            'description': 'Test role description',
            'permissions': ['permission1', 'permission2']
        }
        
        role = Role(role_data)
        
        # Test accessing properties via camelCase (direct schema field names)
        assert role.identifier == 'role1'
        assert role.name == 'Test Role'
        assert role.description == 'Test role description'
        assert role.permissions == ['permission1', 'permission2']
        
        # Test accessing properties via snake_case
        assert role.allowed_scope_levels is None
        
        # Test accessing non-existent property
        with pytest.raises(AttributeError):
            role.non_existent_property

    def test_export_dict(self):
        """
        Test exporting role data as a dictionary
        """
        role_data = {
            'identifier': 'role1',
            'name': 'Test Role',
            'description': 'Test role description',
            'permissions': ['permission1', 'permission2']
        }
        
        role = Role(role_data)
        exported_data = role.export_dict()
        
        # Verify exported data contains all original fields
        assert exported_data['identifier'] == 'role1'
        assert exported_data['name'] == 'Test Role'
        assert exported_data['description'] == 'Test role description'
        assert exported_data['permissions'] == ['permission1', 'permission2']
        
        # Verify fields that weren't in the original data are None in the export
        assert 'allowed_scope_levels' in exported_data
        assert exported_data['allowed_scope_levels'] is None
