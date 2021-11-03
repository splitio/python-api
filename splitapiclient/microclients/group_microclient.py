from splitapiclient.resources import Group
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class GroupMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'groups?limit=200&offset={offset}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'create_group': {
            'method': 'POST',
            'url_template': ('groups'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'delete_group': {
            'method': 'DELETE',
            'url_template': ('groups/{groupId}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'update_group': {
            'method': 'PUT',
            'url_template': ('groups/{groupId}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
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
        Returns a list of Group objects.

        :returns: list of Group objects
        :rtype: list(Group)
        '''
        offset_val = 0
        final_list = []
        while True:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                offset = offset_val
            )
            for item in response['objects']:
                final_list.append(as_dict(item))
            offset = int(response['offset'])
            totalCount = int(response['totalCount'])
            limit = int(response['limit'])
            if totalCount>(offset+limit):
                offset_val = offset_val + limit
                continue
            else:
                break
        return [Group(item, self._http_client) for item in final_list]

    def find(self, group_name):
        '''
        Find Group in list objects.

        :returns: Group object
        :rtype: Group
        '''
        for item in self.list():
            if item._name == group_name:
                return item
        return None

    def create_group(self, data):
        '''
        create new group

        :param: group name and description

        :returns: Group object
        :rtype: Group
        '''
        response = self._http_client.make_request(
            self._endpoint['create_group'],
            body = data
        )
        return Group(response)

    def delete_group(self, group_id):
        '''
        delete a group

        :param: group id

        :returns: True if successful
        :rtype: Boolean
        '''
        response = self._http_client.make_request(
            self._endpoint['delete_group'],
            groupId = group_id
        )
        return True

    def update_group(self, group_id, data):
        '''
        update group data

        :param: group id, name and description

        :returns: Group object
        :rtype: Group
        '''
        response = self._http_client.make_request(
            self._endpoint['update_group'],
            groupId = group_id,
            body=as_dict(data)
        )
        return Group(response)

