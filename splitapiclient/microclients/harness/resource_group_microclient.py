from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import ResourceGroup
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class ResourceGroupMicroClient:
    '''
    Microclient for managing Harness resource groups
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'resourceGroups',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_resource_group': {
            'method': 'GET',
            'url_template': 'resourceGroups/{resourceGroupId}',
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
            'url_template': 'resourceGroups',
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
            'url_template': 'resourceGroups/{resourceGroupId}',
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
            'url_template': 'resourceGroups/{resourceGroupId}',
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
        Returns a list of ResourceGroup objects.

        :returns: list of ResourceGroup objects
        :rtype: list(ResourceGroup)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items']
        )
        return [ResourceGroup(item, self._http_client) for item in response.get('items', [])]

    def get(self, resource_group_id):
        '''
        Get a specific resource group by ID

        :param resource_group_id: ID of the resource group to retrieve
        :returns: ResourceGroup object
        :rtype: ResourceGroup
        '''
        response = self._http_client.make_request(
            self._endpoint['get_resource_group'],
            resourceGroupId=resource_group_id
        )
        return ResourceGroup(response, self._http_client)

    def create(self, resource_group_data):
        '''
        Create a new resource group

        :param resource_group_data: Dictionary containing resource group data
        :returns: newly created resource group
        :rtype: ResourceGroup
        '''
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=resource_group_data
        )
        return ResourceGroup(response, self._http_client)

    def update(self, resource_group_id, update_data):
        '''
        Update a resource group

        :param resource_group_id: ID of the resource group to update
        :param update_data: Dictionary containing update data
        :returns: updated resource group
        :rtype: ResourceGroup
        '''
        response = self._http_client.make_request(
            self._endpoint['update'],
            body=update_data,
            resourceGroupId=resource_group_id
        )
        return ResourceGroup(response, self._http_client)

    def delete(self, resource_group_id):
        '''
        Delete a resource group

        :param resource_group_id: ID of the resource group to delete
        :returns: True if successful
        :rtype: bool
        '''
        self._http_client.make_request(
            self._endpoint['delete'],
            resourceGroupId=resource_group_id
        )
        return True
