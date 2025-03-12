from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import HarnessGroup
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class HarnessGroupMicroClient:
    '''
    Microclient for managing Harness groups
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'harness/groups',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_group': {
            'method': 'GET',
            'url_template': 'harness/groups/{groupId}',
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
            'url_template': 'harness/groups',
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
            'url_template': 'harness/groups/{groupId}',
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
            'url_template': 'harness/groups/{groupId}',
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
        Returns a list of HarnessGroup objects.

        :returns: list of HarnessGroup objects
        :rtype: list(HarnessGroup)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items']
        )
        return [HarnessGroup(item, self._http_client) for item in response.get('items', [])]

    def get(self, group_id):
        '''
        Get a specific group by ID

        :param group_id: ID of the group to retrieve
        :returns: HarnessGroup object
        :rtype: HarnessGroup
        '''
        response = self._http_client.make_request(
            self._endpoint['get_group'],
            groupId=group_id
        )
        return HarnessGroup(response, self._http_client)

    def create(self, group_data):
        '''
        Create a new group

        :param group_data: Dictionary containing group data
        :returns: newly created group
        :rtype: HarnessGroup
        '''
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=group_data
        )
        return HarnessGroup(response, self._http_client)

    def update(self, group_id, update_data):
        '''
        Update a group

        :param group_id: ID of the group to update
        :param update_data: Dictionary containing update data
        :returns: updated group
        :rtype: HarnessGroup
        '''
        response = self._http_client.make_request(
            self._endpoint['update'],
            body=update_data,
            groupId=group_id
        )
        return HarnessGroup(response, self._http_client)

    def delete(self, group_id):
        '''
        Delete a group

        :param group_id: ID of the group to delete
        :returns: True if successful
        :rtype: bool
        '''
        self._http_client.make_request(
            self._endpoint['delete'],
            groupId=group_id
        )
        return True
