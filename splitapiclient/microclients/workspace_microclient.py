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
            'url_template': 'workspaces',
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
        response = self._http_client.make_request(
            self._endpoint['all_items']
        )
        return [Workspace(item, self._http_client) for item in response['objects']]
