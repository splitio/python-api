from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import ServiceAccount
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestServiceAccount:
    """
    Tests for the ServiceAccount resource class
    """

    def test_initialization(self):
        """
        Test initialization of a ServiceAccount object
        """
        # Test with empty data
        sa = ServiceAccount()
        assert sa._id is None
        assert sa._identifier is None
        assert sa._name is None
        
        # Test with data
        sa_data = {
            'identifier': 'sa1',
            'name': 'Test Service Account',
            'email': 'sa1@example.com',
            'description': 'Test service account description',
            'tags': {
                'property1': 'value1',
                'property2': 'value2'
            },
            'accountIdentifier': 'test_account',
            'orgIdentifier': 'test_org',
            'projectIdentifier': 'test_project',
            'extendable': True
        }
        
        sa = ServiceAccount(sa_data)
        
        # Verify all properties were set correctly
        assert sa._id == 'sa1'
        assert sa._identifier == 'sa1'
        assert sa._name == 'Test Service Account'
        assert sa._email == 'sa1@example.com'
        assert sa._description == 'Test service account description'
        assert sa._tags == {'property1': 'value1', 'property2': 'value2'}
        assert sa._account_identifier == 'test_account'
        assert sa._org_identifier == 'test_org'
        assert sa._project_identifier == 'test_project'
        assert sa._extendable is True

    def test_getattr(self):
        """
        Test dynamic property access via __getattr__
        """
        sa_data = {
            'identifier': 'sa1',
            'name': 'Test Service Account',
            'email': 'sa1@example.com',
            'accountIdentifier': 'test_account'
        }
        
        sa = ServiceAccount(sa_data)
        
        # Test accessing properties via camelCase (direct schema field names)
        assert sa.identifier == 'sa1'
        assert sa.name == 'Test Service Account'
        assert sa.email == 'sa1@example.com'
        assert sa.accountIdentifier == 'test_account'
        
        # Test accessing properties via snake_case
        assert sa.account_identifier == 'test_account'
        
        # Test accessing non-existent property
        with pytest.raises(AttributeError):
            sa.non_existent_property

    def test_export_dict(self):
        """
        Test exporting service account data as a dictionary
        """
        sa_data = {
            'identifier': 'sa1',
            'name': 'Test Service Account',
            'email': 'sa1@example.com',
            'description': 'Test service account description',
            'accountIdentifier': 'test_account'
        }
        
        sa = ServiceAccount(sa_data)
        exported_data = sa.export_dict()
        
        # Verify exported data contains all original fields
        assert exported_data['identifier'] == 'sa1'
        assert exported_data['name'] == 'Test Service Account'
        assert exported_data['email'] == 'sa1@example.com'
        assert exported_data['description'] == 'Test service account description'
        assert exported_data['accountIdentifier'] == 'test_account'
        
        # Verify fields that weren't in the original data are None in the export
        assert 'projectIdentifier' in exported_data
        assert exported_data['projectIdentifier'] is None
        assert 'orgIdentifier' in exported_data
        assert exported_data['orgIdentifier'] is None
