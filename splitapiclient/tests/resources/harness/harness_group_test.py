from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import HarnessGroup
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestHarnessGroup:
    """
    Tests for the HarnessGroup resource class
    """

    def test_initialization(self):
        """
        Test initialization of a HarnessGroup object
        """
        # Test with empty data
        group = HarnessGroup()
        assert group._id is None
        assert group._identifier is None
        assert group._name is None
        
        # Test with data
        group_data = {
            'identifier': 'group1',
            'name': 'Test Group',
            'description': 'Test group description',
            'accountIdentifier': 'test_account',
            'orgIdentifier': 'test_org',
            'projectIdentifier': 'test_project',
            'users': [
                {
                    'uuid': 'user1',
                    'name': 'User 1',
                    'email': 'user1@example.com'
                }
            ],
            'ssoLinked': False,
            'externallyManaged': False,
            'harnessManaged': True,
            'tags': {
                'property1': 'value1',
                'property2': 'value2'
            }
        }
        
        group = HarnessGroup(group_data)
        
        # Verify all properties were set correctly
        assert group._id == 'group1'
        assert group._identifier == 'group1'
        assert group._name == 'Test Group'
        assert group._description == 'Test group description'
        assert group._account_identifier == 'test_account'
        assert group._org_identifier == 'test_org'
        assert group._project_identifier == 'test_project'
        assert len(group._users) == 1
        assert group._users[0]['uuid'] == 'user1'
        assert group._sso_linked is False
        assert group._externally_managed is False
        assert group._harness_managed is True
        assert group._tags == {'property1': 'value1', 'property2': 'value2'}

    def test_name_property(self):
        """
        Test the name property accessor
        """
        group_data = {
            'identifier': 'group1',
            'name': 'Test Group',
            'accountIdentifier': 'test_account'
        }
        
        group = HarnessGroup(group_data)
        assert group.name == 'Test Group'

    def test_getattr(self):
        """
        Test dynamic property access via __getattr__
        """
        group_data = {
            'identifier': 'group1',
            'name': 'Test Group',
            'description': 'Test group description',
            'accountIdentifier': 'test_account',
            'ssoLinked': False,
            'externallyManaged': False
        }
        
        group = HarnessGroup(group_data)
        
        # Test accessing properties via camelCase (direct schema field names)
        assert group.identifier == 'group1'
        assert group.name == 'Test Group'
        assert group.description == 'Test group description'
        assert group.accountIdentifier == 'test_account'
        assert group.ssoLinked is False
        assert group.externallyManaged is False
        
        # Test accessing properties via snake_case
        assert group.account_identifier == 'test_account'
        assert group.sso_linked is False
        assert group.externally_managed is False
        
        # Test accessing non-existent property
        with pytest.raises(AttributeError):
            group.non_existent_property

    def test_export_dict(self):
        """
        Test exporting group data as a dictionary
        """
        group_data = {
            'identifier': 'group1',
            'name': 'Test Group',
            'description': 'Test group description',
            'accountIdentifier': 'test_account',
            'ssoLinked': False,
            'externallyManaged': False
        }
        
        group = HarnessGroup(group_data)
        exported_data = group.export_dict()
        
        # Verify exported data contains all original fields
        assert exported_data['identifier'] == 'group1'
        assert exported_data['name'] == 'Test Group'
        assert exported_data['description'] == 'Test group description'
        assert exported_data['accountIdentifier'] == 'test_account'
        assert exported_data['ssoLinked'] is False
        assert exported_data['externallyManaged'] is False
        
        # Verify fields that weren't in the original data are None in the export
        assert 'orgIdentifier' in exported_data
        assert exported_data['orgIdentifier'] is None
        assert 'projectIdentifier' in exported_data
        assert exported_data['projectIdentifier'] is None
        assert 'users' in exported_data
        assert exported_data['users'] is None
