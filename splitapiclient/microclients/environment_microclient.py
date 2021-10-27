from splitapiclient.resources import Environment
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class EnvironmentMicroClient:
    '''
    '''
    _endpoint = {
        'create': {
            'method': 'POST',
            'url_template': ('environments/ws/{workspaceId}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'update_name': {
            'method': 'PATCH',
            'url_template': ('environments/ws/{workspaceId}/{environmentName}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'delete': {
            'method': 'DELETE',
            'url_template': ('environments/ws/{workspaceId}/{environmentName}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'all_items': {
            'method': 'GET',
            'url_template': 'environments/ws/{workspaceId}',
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

    def list(self, workspace_id):
        '''
        Returns a list of Environment objects.

        :returns: list of Environment objects
        :rtype: list(Environment)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items'],
            workspaceId = workspace_id
        )
        return [Environment(item, workspace_id, self._http_client) for item in response]

    def find(self, environment_name, workspace_id):
        '''
        Find Environment in environment list objects.

        :returns: Environment objects
        :rtype: Environment
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items'],
            workspaceId = workspace_id
        )
        for item in response:
            if item['name']==environment_name:
                return Environment(item, workspace_id, self._http_client)
        LOGGER.error("Environment Name does not exist")
        return None

    def add(self, environment, workspace_id):
        '''
        add an environment

        :param environment: environment instance or dict containing name and production flag
            properties

        :returns: newly created environment
        :rtype: Environment
        '''
        data = as_dict(environment)
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=data,
            workspaceId = workspace_id
        )
        return Environment(response, workspace_id,  self._http_client)

    def update_name(self, new_name, environment, workspace_id):
        '''
        update environment

        :param environment: environment instance or dict containing name and production flag
            properties

        :returns: updated environment
        :rtype: Environment
        '''
        data = as_dict(environment)
        response = self._http_client.make_request(
            self._endpoint['update_name'],
            body= [as_dict({'op': 'replace', 'path': '/name', 'value':new_name})],
            workspaceId =workspace_id,
            environmentName = data['name']
        )
        return response

    def delete(self, environment_name, workspace_id):
        '''
        delete an environment

        :param environment: environment instance or dict containing name and production flag
            properties

        :returns:
        :rtype: Environment
        '''
        response = self._http_client.make_request(
            self._endpoint['delete'],
            workspaceId =workspace_id,
            environmentName = environment_name
        )
        return response

