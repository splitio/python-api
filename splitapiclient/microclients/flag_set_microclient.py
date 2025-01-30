from splitapiclient.resources.flag_set import FlagSet
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class FlagSetMicroClient:
    '''
    '''
    _endpoint = {
        'list_initial': {
            'method': 'GET',
            'url_template': 'flag-sets?workspace_id={workspace_id}&limit=50',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'list_next': {
            'method': 'GET',
            'url_template': 'flag-sets?workspace_id={workspace_id}&after={after}&limit=50',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get': {
            'method': 'GET',
            'url_template': 'flag-sets/{flag_set_id}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'create': {
            'method': 'POST',
            'url_template': 'flag-sets',
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
            'url_template': ('flag-sets/{flagSetId}'),
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
        Returns a list of flag_sets objects.

        :returns: list of flag_sets objects
        :rtype: list(flag_sets)
        '''
        final_list = []
        afterMarker = 0
        while True:
            if afterMarker==0:
                response = self._http_client.make_request(
                    self._endpoint['list_initial'],
                    workspace_id = workspace_id
                )
            else:
                response = self._http_client.make_request(
                    self._endpoint['list_next'],
                    workspace_id = workspace_id,
                    after = afterMarker
                )
            for item in response['data']:
                final_list.append(as_dict(item))
            if response['nextMarker'] is None:
                break
            else:
                afterMarker = response['nextMarker']
                continue
        return [FlagSet(item, workspace_id, self._http_client) for item in final_list]
        
    def find(self, flag_set_name=None, workspace_id=None):
        '''
        Search for flag_set in list of flag_sets objects.

        :returns: flag_set object
        :rtype: flag_set
        '''

        for item in self.list(workspace_id=workspace_id):
            if item.name==flag_set_name:
                return item
        LOGGER.error("flag_set Name does not exist")
        return None
    
    def get(self, flag_set_id=None):
        '''
        get a flag_set

        :param flag_set_id: flag_set id
        :returns: flag_set
        :rtype: flag_set
        '''

        response = self._http_client.make_request(
            self._endpoint['get'],
            flag_set_id=flag_set_id
        )
        return FlagSet(data=response,  client=self._http_client)

        


    def add(self, flag_set, workspace_id):
        '''
        add a flag_set

        :param flag_set: flag_set instance
        :returns: newly created flag_set
        :rtype: flag_set
        '''
        data = as_dict(flag_set)
        data['workspace'] = {
            'id': workspace_id,
            'type': 'WORKSPACE'
        }
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=data
        )
        return FlagSet(response, workspace_id, self._http_client)



    def delete(self, flag_set_id ):
        '''
        delete a flag_set

        :param flag_set id:

        :returns:
        :rtype: True if successful
        '''
        response = self._http_client.make_request(
            self._endpoint['delete'],
            flagSetId =flag_set_id,
        )
        return response
