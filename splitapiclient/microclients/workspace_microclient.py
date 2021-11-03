from splitapiclient.resources import Workspace
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER

class WorkspaceMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'workspaces?limit=20&offset={offset}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_rollout_statuses': {
            'method': 'GET',
            'url_template': 'rolloutStatuses?wsId={workspaceId}',
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
        Returns a list of Workspaces objects.

        :returns: list of Workspaces objects
        :rtype: list(Workspaces)
        '''
        offset_val = 0
        final_list = []
        while True:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                offset = offset_val
            )
            for item in response['objects']:
                final_list.append(item)
            offset = int(response['offset'])
            totalCount = int(response['totalCount'])
            limit = int(response['limit'])
            if totalCount>(offset+limit):
                offset_val = offset_val + limit
                continue
            else:
                break
        return [Workspace(item, self._http_client) for item in final_list]
        
    def find(self, workspace_name=None):
        '''
        Search for workspace in list of Workspaces objects.

        :returns: workspace object
        :rtype: Workspace
        '''

        for item in self.list():
            if item.name==workspace_name:
                return item
        LOGGER.error("Workspace Name does not exist")
        return None
        
    def get_rollout_statuses(self, workspace_id):
        '''
        get rollout statuses list

        :returns: rollout status list
        :rtype: Dict
        '''
        
        response = self._http_client.make_request(
            self._endpoint['get_rollout_statuses'],
            workspaceId = workspace_id
        )
        return response
