from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import ResourceGroup
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestResourceGroup:
    """
    Tests for the ResourceGroup resource class
    """

    def test_initialization(self):
        """
        Test initialization of a ResourceGroup object
        """
        # Test with empty data
        resource_group = ResourceGroup()
        assert resource_group._id is None
        assert resource_group._identifier is None
        assert resource_group._name is None
        
        # Test with data
        resource_group_data = {
            'identifier': 'rg1',
            'name': 'Test Resource Group',
            'description': 'Test resource group description',
            'accountIdentifier': 'test_account',
            'orgIdentifier': 'test_org',
            'projectIdentifier': 'test_project',
            'color': '#FF0000',
            'tags': {
                'property1': 'value1',
                'property2': 'value2'
            },
            'allowedScopeLevels': ['account', 'project'],
            'includedScopes': [
                {
                    'filter': 'filter1',
                    'accountIdentifier': 'test_account',
                    'orgIdentifier': 'test_org',
                    'projectIdentifier': 'test_project'
                }
            ],
            'resourceFilter': {
                'resources': [
                    {
                        'resourceType': 'FEATURE_FLAG',
                        'identifiers': ['flag1', 'flag2'],
                        'attributeFilter': {
                            'attributeName': 'attr1',
                            'attributeValues': ['val1', 'val2']
                        }
                    }
                ],
                'includeAllResources': False
            }
        }
        
        resource_group = ResourceGroup(resource_group_data)
        
        # Verify all properties were set correctly
        assert resource_group._id == 'rg1'
        assert resource_group._identifier == 'rg1'
        assert resource_group._name == 'Test Resource Group'
        assert resource_group._description == 'Test resource group description'
        assert resource_group._account_identifier == 'test_account'
        assert resource_group._org_identifier == 'test_org'
        assert resource_group._project_identifier == 'test_project'
        assert resource_group._color == '#FF0000'
        assert resource_group._tags == {'property1': 'value1', 'property2': 'value2'}
        assert resource_group._allowed_scope_levels == ['account', 'project']
        assert len(resource_group._included_scopes) == 1
        assert resource_group._included_scopes[0]['filter'] == 'filter1'
        assert resource_group._resource_filter['includeAllResources'] is False
        assert len(resource_group._resource_filter['resources']) == 1
        assert resource_group._resource_filter['resources'][0]['resourceType'] == 'FEATURE_FLAG'

    def test_getattr(self):
        """
        Test dynamic property access via __getattr__
        """
        resource_group_data = {
            'identifier': 'rg1',
            'name': 'Test Resource Group',
            'description': 'Test resource group description',
            'accountIdentifier': 'test_account',
            'resourceFilter': {
                'includeAllResources': False,
                'resources': []
            }
        }
        
        resource_group = ResourceGroup(resource_group_data)
        
        # Test accessing properties via camelCase (direct schema field names)
        assert resource_group.identifier == 'rg1'
        assert resource_group.name == 'Test Resource Group'
        assert resource_group.description == 'Test resource group description'
        assert resource_group.accountIdentifier == 'test_account'
        assert resource_group.resourceFilter['includeAllResources'] is False
        
        # Test accessing properties via snake_case
        assert resource_group.account_identifier == 'test_account'
        assert resource_group.resource_filter['includeAllResources'] is False
        
        # Test accessing non-existent property
        with pytest.raises(AttributeError):
            resource_group.non_existent_property

    def test_export_dict(self):
        """
        Test exporting resource group data as a dictionary
        """
        resource_group_data = {
            'identifier': 'rg1',
            'name': 'Test Resource Group',
            'description': 'Test resource group description',
            'accountIdentifier': 'test_account',
            'resourceFilter': {
                'includeAllResources': False,
                'resources': []
            }
        }
        
        resource_group = ResourceGroup(resource_group_data)
        exported_data = resource_group.export_dict()
        
        # Verify exported data contains all original fields
        assert exported_data['identifier'] == 'rg1'
        assert exported_data['name'] == 'Test Resource Group'
        assert exported_data['description'] == 'Test resource group description'
        assert exported_data['accountIdentifier'] == 'test_account'
        assert exported_data['resourceFilter']['includeAllResources'] is False
        
        # Verify fields that weren't in the original data are None in the export
        assert 'orgIdentifier' in exported_data
        assert exported_data['orgIdentifier'] is None
        assert 'projectIdentifier' in exported_data
        assert exported_data['projectIdentifier'] is None
        assert 'color' in exported_data
        assert exported_data['color'] is None
