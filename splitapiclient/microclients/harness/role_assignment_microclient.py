from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import RoleAssignment
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class RoleAssignmentMicroClient:
    '''
    Microclient for managing Harness role assignments
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'roleAssignments',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_role_assignment': {
            'method': 'GET',
            'url_template': 'roleAssignments/{roleAssignmentId}',
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
            'url_template': 'roleAssignments',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'update': {
            'method': 'PATCH',
            'url_template': 'roleAssignments/{roleAssignmentId}',
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
            'url_template': 'roleAssignments/{roleAssignmentId}',
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

    def list(self):
        '''
        Returns a list of RoleAssignment objects.

        :returns: list of RoleAssignment objects
        :rtype: list(RoleAssignment)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items']
        )
        return [RoleAssignment(item, self._http_client) for item in response.get('items', [])]

    def get(self, role_assignment_id):
        '''
        Get a specific role assignment by ID

        :param role_assignment_id: ID of the role assignment to retrieve
        :returns: RoleAssignment object
        :rtype: RoleAssignment
        '''
        response = self._http_client.make_request(
            self._endpoint['get_role_assignment'],
            roleAssignmentId=role_assignment_id
        )
        return RoleAssignment(response, self._http_client)

    def create(self, role_assignment_data):
        '''
        Create a new role assignment

        :param role_assignment_data: Dictionary containing role assignment data
        :returns: newly created role assignment
        :rtype: RoleAssignment
        '''
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=role_assignment_data
        )
        return RoleAssignment(response, self._http_client)

    def update(self, role_assignment_id, update_data):
        '''
        Update a role assignment

        :param role_assignment_id: ID of the role assignment to update
        :param update_data: Dictionary containing update data
        :returns: updated role assignment
        :rtype: RoleAssignment
        '''
        response = self._http_client.make_request(
            self._endpoint['update'],
            body=update_data,
            roleAssignmentId=role_assignment_id
        )
        return RoleAssignment(response, self._http_client)

    def delete(self, role_assignment_id):
        '''
        Delete a role assignment

        :param role_assignment_id: ID of the role assignment to delete
        :returns: True if successful
        :rtype: bool
        '''
        self._http_client.make_request(
            self._endpoint['delete'],
            roleAssignmentId=role_assignment_id
        )
        return True
