from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import HarnessProject
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class HarnessProjectMicroClient:
    '''
    Microclient for managing Harness projects
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'projects',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_project': {
            'method': 'GET',
            'url_template': 'projects/{projectId}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'create': {
            'method': 'POST',
            'url_template': 'projects',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'update': {
            'method': 'PUT',
            'url_template': 'projects/{projectId}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'delete': {
            'method': 'DELETE',
            'url_template': 'projects/{projectId}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
    }

    def __init__(self, http_client):
        '''
        Constructor
        '''
        self._http_client = http_client

    def list(self, account_id=None, org_id=None):
        '''
        Returns a list of HarnessProject objects.

        :param account_id: Optional account identifier to filter projects
        :param org_id: Optional organization identifier to filter projects
        :returns: list of HarnessProject objects
        :rtype: list(HarnessProject)
        '''
        query_params = {}
        if account_id:
            query_params['accountIdentifier'] = account_id
        if org_id:
            query_params['orgIdentifier'] = org_id
            
        response = self._http_client.make_request(
            self._endpoint['all_items'],
            query_params=query_params
        )
        return [HarnessProject(item, self._http_client) for item in response.get('items', [])]

    def get(self, project_id, account_id=None, org_id=None):
        '''
        Get a specific project by ID

        :param project_id: ID of the project to retrieve
        :param account_id: Optional account identifier
        :param org_id: Optional organization identifier
        :returns: HarnessProject object
        :rtype: HarnessProject
        '''
        query_params = {}
        if account_id:
            query_params['accountIdentifier'] = account_id
        if org_id:
            query_params['orgIdentifier'] = org_id
            
        response = self._http_client.make_request(
            self._endpoint['get_project'],
            projectId=project_id,
            query_params=query_params
        )
        return HarnessProject(response, self._http_client)

    def create(self, project_data):
        '''
        Create a new project

        :param project_data: Dictionary containing project data
        :returns: newly created project
        :rtype: HarnessProject
        '''
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=project_data
        )
        return HarnessProject(response, self._http_client)

    def update(self, project_id, project_data):
        '''
        Update an existing project

        :param project_id: ID of the project to update
        :param project_data: Dictionary containing updated project data
        :returns: updated project
        :rtype: HarnessProject
        '''
        response = self._http_client.make_request(
            self._endpoint['update'],
            projectId=project_id,
            body=project_data
        )
        return HarnessProject(response, self._http_client)

    def delete(self, project_id, account_id=None, org_id=None):
        '''
        Delete a project

        :param project_id: ID of the project to delete
        :param account_id: Optional account identifier
        :param org_id: Optional organization identifier
        :returns: True if successful
        :rtype: bool
        '''
        query_params = {}
        if account_id:
            query_params['accountIdentifier'] = account_id
        if org_id:
            query_params['orgIdentifier'] = org_id
            
        self._http_client.make_request(
            self._endpoint['delete'],
            projectId=project_id,
            query_params=query_params
        )
        return True
