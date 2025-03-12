from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import Role
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class RoleMicroClient:
    '''
    Microclient for managing Harness roles
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'roles',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_role': {
            'method': 'GET',
            'url_template': 'roles/{roleId}',
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
            'url_template': 'roles',
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
            'url_template': 'roles/{roleId}',
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
            'url_template': 'roles/{roleId}',
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
        Returns a list of Role objects.

        :returns: list of Role objects
        :rtype: list(Role)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items']
        )
        return [Role(item, self._http_client) for item in response.get('items', [])]

    def get(self, role_id):
        '''
        Get a specific role by ID

        :param role_id: ID of the role to retrieve
        :returns: Role object
        :rtype: Role
        '''
        response = self._http_client.make_request(
            self._endpoint['get_role'],
            roleId=role_id
        )
        return Role(response, self._http_client)

    def create(self, role_data):
        '''
        Create a new role

        :param role_data: Dictionary containing role data
        :returns: newly created role
        :rtype: Role
        '''
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=role_data
        )
        return Role(response, self._http_client)

    def update(self, role_id, update_data):
        '''
        Update a role

        :param role_id: ID of the role to update
        :param update_data: Dictionary containing update data
        :returns: updated role
        :rtype: Role
        '''
        response = self._http_client.make_request(
            self._endpoint['update'],
            body=update_data,
            roleId=role_id
        )
        return Role(response, self._http_client)

    def delete(self, role_id):
        '''
        Delete a role

        :param role_id: ID of the role to delete
        :returns: True if successful
        :rtype: bool
        '''
        self._http_client.make_request(
            self._endpoint['delete'],
            roleId=role_id
        )
        return True
