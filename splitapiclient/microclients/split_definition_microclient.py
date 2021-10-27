from splitapiclient.resources import SplitDefinition
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class SplitDefinitionMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'splits/ws/{workspaceId}/environments/{environmentId}?limit=20&offset={offset}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'update_definition': {
            'method': 'PUT',
            'url_template': ('splits/ws/{workspaceId}/{splitName}/environments/{environmentId}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'kill': {
            'method': 'PUT',
            'url_template': ('splits/ws/{workspaceId}/{splitName}/environments/{environmentId}/kill'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'restore': {
            'method': 'PUT',
            'url_template': ('splits/ws/{workspaceId}/{splitName}/environments/{environmentId}/restore'),
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

    def list(self, environment_id, workspace_id):
        '''
        Returns a list of Split definitions objects.

        :returns: list of Split definitions objects
        :rtype: list(SplitDefinition)
        '''
        offset_val = 0
        final_list = []
        while True:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                workspaceId = workspace_id,
                environmentId = environment_id,
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
        return [SplitDefinition(item, environment_id, workspace_id, self._http_client) for item in final_list]

    def find(self, split_name, environment_id, workspace_id):
        '''
        Find Split definition in environment objects.

        :returns: SplitDefinition object
        :rtype: SplitDefinition
        '''
        for item in self.list(environment_id, workspace_id):
            if item.name == split_name:
                return item
        LOGGER.error("Split Name does not exist")
        return None

    def update_definition(self, split_name, environment_id, workspace_id, new_definition):
        '''
        update a split definition

        :param split: split name, environment id, workspace id and new definition
        
        :returns: updated split definition
        :rtype: SplitDefinition
        '''
        
        response = self._http_client.make_request(
            self._endpoint['update_definition'],
            body=new_definition,
            environmentId = environment_id,
            workspaceId = workspace_id,
            splitName = split_name
        )
        return SplitDefinition(response, environment_id, workspace_id, self._http_client)

    def kill(self, split_name, environment_id, workspace_id):
        '''
        kill a split

        :param split: split name, environment id, workspace id
        
        :returns: True if successful
        :rtype: Boolean
        '''
        
        response = self._http_client.make_request(
            self._endpoint['kill'],
            environmentId = environment_id,
            workspaceId = workspace_id,
            splitName = split_name
        )
        return response

    def restore(self, split_name, environment_id, workspace_id):
        '''
        restore a split

        :param split: split name, environment id, workspace id
        
        :returns: True if successful
        :rtype: Boolean
        '''
        
        response = self._http_client.make_request(
            self._endpoint['restore'],
            environmentId = environment_id,
            workspaceId = workspace_id,
            splitName = split_name
        )
        return response

