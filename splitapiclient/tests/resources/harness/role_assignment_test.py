from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import RoleAssignment
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestRoleAssignment:
    """
    Tests for the RoleAssignment resource class
    """

    def test_initialization(self):
        """
        Test initialization of a RoleAssignment object
        """
        # Test with empty data
        role_assignment = RoleAssignment()
        assert role_assignment._id is None
        assert role_assignment._identifier is None
        assert role_assignment._role_identifier is None
        
        # Test with data
        role_assignment_data = {
            'identifier': 'ra1',
            'resourceGroupIdentifier': 'rg1',
            'roleIdentifier': 'role1',
            'roleReference': {
                'identifier': 'role1',
                'scopeLevel': 'account'
            },
            'principal': {
                'scopeLevel': 'account',
                'identifier': 'user1',
                'type': 'USER',
                'uniqueId': 'unique1'
            },
            'disabled': False,
            'managed': True,
            'internal': False
        }
        
        role_assignment = RoleAssignment(role_assignment_data)
        
        # Verify all properties were set correctly
        assert role_assignment._id == 'ra1'
        assert role_assignment._identifier == 'ra1'
        assert role_assignment._resource_group_identifier == 'rg1'
        assert role_assignment._role_identifier == 'role1'
        assert role_assignment._role_reference == {
            'identifier': 'role1',
            'scopeLevel': 'account'
        }
        assert role_assignment._principal == {
            'scopeLevel': 'account',
            'identifier': 'user1',
            'type': 'USER',
            'uniqueId': 'unique1'
        }
        assert role_assignment._disabled is False
        assert role_assignment._managed is True
        assert role_assignment._internal is False

    def test_getattr(self):
        """
        Test dynamic property access via __getattr__
        """
        role_assignment_data = {
            'identifier': 'ra1',
            'resourceGroupIdentifier': 'rg1',
            'roleIdentifier': 'role1',
            'principal': {
                'identifier': 'user1',
                'type': 'USER'
            },
            'disabled': False
        }
        
        role_assignment = RoleAssignment(role_assignment_data)
        
        # Test accessing properties via camelCase (direct schema field names)
        assert role_assignment.identifier == 'ra1'
        assert role_assignment.resourceGroupIdentifier == 'rg1'
        assert role_assignment.roleIdentifier == 'role1'
        assert role_assignment.principal == {
            'identifier': 'user1',
            'type': 'USER'
        }
        assert role_assignment.disabled is False
        
        # Test accessing properties via snake_case
        assert role_assignment.resource_group_identifier == 'rg1'
        assert role_assignment.role_identifier == 'role1'
        
        # Test accessing non-existent property
        with pytest.raises(AttributeError):
            role_assignment.non_existent_property

    def test_export_dict(self):
        """
        Test exporting role assignment data as a dictionary
        """
        role_assignment_data = {
            'identifier': 'ra1',
            'resourceGroupIdentifier': 'rg1',
            'roleIdentifier': 'role1',
            'principal': {
                'identifier': 'user1',
                'type': 'USER'
            },
            'disabled': False
        }
        
        role_assignment = RoleAssignment(role_assignment_data)
        exported_data = role_assignment.export_dict()
        
        # Verify exported data contains all original fields
        assert exported_data['identifier'] == 'ra1'
        assert exported_data['resourceGroupIdentifier'] == 'rg1'
        assert exported_data['roleIdentifier'] == 'role1'
        assert exported_data['principal'] == {
            'identifier': 'user1',
            'type': 'USER'
        }
        assert exported_data['disabled'] is False
        
        # Verify fields that weren't in the original data are None in the export
        assert 'roleReference' in exported_data
        assert exported_data['roleReference'] is None
        assert 'managed' in exported_data
        assert exported_data['managed'] is None
        assert 'internal' in exported_data
        assert exported_data['internal'] is None
