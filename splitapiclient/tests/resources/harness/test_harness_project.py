from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.harness import HarnessProject
from splitapiclient.http_clients.harness_client import HarnessHttpClient


class TestHarnessProject:
    '''
    Tests for the HarnessProject class' methods
    '''
    def test_constructor(self, mocker):
        '''
        Test that the constructor properly initializes the HarnessProject object
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'splitapiclient.resources.base_resource.BaseResource.__init__',
            new=mock_init
        )
        
        project_data = {
            'identifier': 'project-123',
            'name': 'Test Project',
            'description': 'A test project',
            'orgIdentifier': 'org-123',
            'color': '#FF0000',
            'modules': ['module1', 'module2'],
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        project = HarnessProject(project_data, client)
        
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(project, 'project-123', client)

    def test_getters(self):
        '''
        Test that getters properly return the values from the HarnessProject object
        '''
        project_data = {
            'identifier': 'project-123',
            'name': 'Test Project',
            'description': 'A test project',
            'orgIdentifier': 'org-123',
            'color': '#FF0000',
            'modules': ['module1', 'module2'],
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        project = HarnessProject(project_data)
        
        assert project.identifier == 'project-123'
        assert project.name == 'Test Project'
        assert project.description == 'A test project'
        assert project.org_identifier == 'org-123'
        assert project.color == '#FF0000'
        assert project.modules == ['module1', 'module2']
        assert project.tags == {'key1': 'value1', 'key2': 'value2'}

    def test_export_dict(self):
        '''
        Test that export_dict properly returns a dictionary with the HarnessProject data
        '''
        project_data = {
            'identifier': 'project-123',
            'name': 'Test Project',
            'description': 'A test project',
            'orgIdentifier': 'org-123',
            'color': '#FF0000',
            'modules': ['module1', 'module2'],
            'tags': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        
        project = HarnessProject(project_data)
        exported_data = project.export_dict()
        
        assert exported_data['identifier'] == 'project-123'
        assert exported_data['name'] == 'Test Project'
        assert exported_data['description'] == 'A test project'
        assert exported_data['orgIdentifier'] == 'org-123'
        assert exported_data['color'] == '#FF0000'
        assert exported_data['modules'] == ['module1', 'module2']
        assert exported_data['tags'] == {'key1': 'value1', 'key2': 'value2'}

    def test_missing_attribute(self):
        '''
        Test that accessing a non-existent attribute raises an AttributeError
        '''
        project = HarnessProject({'identifier': 'project-123'})
        
        with pytest.raises(AttributeError):
            project.non_existent_attribute
