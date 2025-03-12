from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import HarnessUser
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class HarnessUserMicroClient:
    '''
    Microclient for managing Harness users
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'harness/users',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_user': {
            'method': 'GET',
            'url_template': 'harness/users/{userId}',
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
            'url_template': 'harness/users',
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
            'url_template': 'harness/users/{userId}',
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
            'url_template': 'harness/users/{userId}',
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
        Returns a list of HarnessUser objects.

        :returns: list of HarnessUser objects
        :rtype: list(HarnessUser)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items']
        )
        return [HarnessUser(item, self._http_client) for item in response.get('items', [])]

    def get(self, user_id):
        '''
        Get a specific user by ID

        :param user_id: ID of the user to retrieve
        :returns: HarnessUser object
        :rtype: HarnessUser
        '''
        response = self._http_client.make_request(
            self._endpoint['get_user'],
            userId=user_id
        )
        return HarnessUser(response, self._http_client)

    def create(self, user_data):
        '''
        Create a new user

        :param user_data: Dictionary containing user data
        :returns: newly created user
        :rtype: HarnessUser
        '''
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=user_data
        )
        return HarnessUser(response, self._http_client)

    def update(self, user_id, update_data):
        '''
        Update a user

        :param user_id: ID of the user to update
        :param update_data: Dictionary containing update data
        :returns: updated user
        :rtype: HarnessUser
        '''
        response = self._http_client.make_request(
            self._endpoint['update'],
            body=update_data,
            userId=user_id
        )
        return HarnessUser(response, self._http_client)

    def delete(self, user_id):
        '''
        Delete a user

        :param user_id: ID of the user to delete
        :returns: True if successful
        :rtype: bool
        '''
        self._http_client.make_request(
            self._endpoint['delete'],
            userId=user_id
        )
        return True
