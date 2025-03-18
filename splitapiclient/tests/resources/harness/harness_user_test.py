from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import HarnessUser
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestHarnessUser:
    """
    Tests for the HarnessUser resource class
    """

    def test_initialization(self):
        """
        Test initialization of a HarnessUser object
        """
        # Test with empty data
        user = HarnessUser()
        assert user._id is None
        assert user._name is None
        assert user._email is None
        
        # Test with data
        user_data = {
            'uuid': 'user1',
            'name': 'Test User',
            'email': 'user@example.com',
            'locked': False,
            'disabled': False,
            'externally_managed': False,
            'two_factor_authentication_enabled': True
        }
        
        user = HarnessUser(user_data)
        
        # Verify all properties were set correctly
        assert user._id == 'user1'
        assert user._name == 'Test User'
        assert user._email == 'user@example.com'
        assert user._locked is False
        assert user._disabled is False
        assert user._externally_managed is False
        assert user._two_factor_authentication_enabled is True

    def test_name_property(self):
        """
        Test the name property accessor
        """
        user_data = {
            'uuid': 'user1',
            'name': 'Test User',
            'email': 'user@example.com'
        }
        
        user = HarnessUser(user_data)
        assert user.name == 'Test User'

    def test_getattr(self):
        """
        Test dynamic property access via __getattr__
        """
        user_data = {
            'uuid': 'user1',
            'name': 'Test User',
            'email': 'user@example.com',
            'locked': False,
            'disabled': False
        }
        
        user = HarnessUser(user_data)
        
        # Test accessing properties via direct schema field names
        assert user.uuid == 'user1'
        assert user.email == 'user@example.com'
        assert user.locked is False
        assert user.disabled is False
        
        # Test accessing properties via snake_case
        assert user.two_factor_authentication_enabled is None
        
        # Test accessing non-existent property
        with pytest.raises(AttributeError):
            user.non_existent_property

    def test_export_dict(self):
        """
        Test exporting user data as a dictionary
        """
        user_data = {
            'uuid': 'user1',
            'name': 'Test User',
            'email': 'user@example.com',
            'locked': False,
            'disabled': False
        }
        
        user = HarnessUser(user_data)
        exported_data = user.export_dict()
        
        # Verify exported data contains all original fields
        assert exported_data['uuid'] == 'user1'
        assert exported_data['name'] == 'Test User'
        assert exported_data['email'] == 'user@example.com'
        assert exported_data['locked'] is False
        assert exported_data['disabled'] is False
        
        # Verify fields that weren't in the original data are None in the export
        assert 'externally_managed' in exported_data
        assert exported_data['externally_managed'] is None
        assert 'two_factor_authentication_enabled' in exported_data
        assert exported_data['two_factor_authentication_enabled'] is None
