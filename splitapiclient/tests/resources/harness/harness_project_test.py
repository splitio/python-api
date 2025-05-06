from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import HarnessProject
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestHarnessProject:
    """
    Tests for the HarnessProject resource class
    """

    def test_initialization(self):
        """
        Test initialization of a HarnessProject object
        """
        # Test with empty data
        project = HarnessProject()
        assert project._id is None
        assert project._identifier is None
        assert project._name is None
        
        # Test with data
        project_data = {
            'identifier': 'project1',
            'name': 'Test Project',
            'description': 'Test project description',
            'orgIdentifier': 'test_org',
            'color': '#FF0000',
            'modules': ['FF', 'CI', 'CD'],
            'tags': {
                'property1': 'value1',
                'property2': 'value2'
            }
        }
        
        project = HarnessProject(project_data)
        
        # Verify all properties were set correctly
        assert project._id == 'project1'
        assert project._identifier == 'project1'
        assert project._name == 'Test Project'
        assert project._description == 'Test project description'
        assert project._org_identifier == 'test_org'
        assert project._color == '#FF0000'
        assert project._modules == ['FF', 'CI', 'CD']
        assert project._tags == {'property1': 'value1', 'property2': 'value2'}

    def test_getattr(self):
        """
        Test dynamic property access via __getattr__
        """
        project_data = {
            'identifier': 'project1',
            'name': 'Test Project',
            'description': 'Test project description',
            'orgIdentifier': 'test_org',
            'color': '#FF0000'
        }
        
        project = HarnessProject(project_data)
        
        # Test accessing properties via snake_case
        assert project.identifier == 'project1'
        assert project.name == 'Test Project'
        assert project.description == 'Test project description'
        assert project.org_identifier == 'test_org'
        assert project.color == '#FF0000'
        
        # Test accessing non-existent property
        with pytest.raises(AttributeError):
            project.non_existent_property

    def test_export_dict(self):
        """
        Test exporting project data as a dictionary
        """
        project_data = {
            'identifier': 'project1',
            'name': 'Test Project',
            'description': 'Test project description',
            'orgIdentifier': 'test_org',
            'color': '#FF0000'
        }
        
        project = HarnessProject(project_data)
        exported_data = project.export_dict()
        
        # Verify exported data contains all original fields
        assert exported_data['identifier'] == 'project1'
        assert exported_data['name'] == 'Test Project'
        assert exported_data['description'] == 'Test project description'
        assert exported_data['orgIdentifier'] == 'test_org'
        assert exported_data['color'] == '#FF0000'
        
        # Verify fields that weren't in the original data are None in the export
        assert 'modules' in exported_data
        assert exported_data['modules'] is None
        assert 'tags' in exported_data
        assert exported_data['tags'] is None
