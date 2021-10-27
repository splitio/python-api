from splitapiclient.resources import APIKey
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class APIKeyMicroClient:
    '''
    '''
    _endpoint = {
        'create_apikey': {
            'method': 'POST',
            'url_template': ('apiKeys'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'delete_apikey': {
            'method': 'DELETE',
            'url_template': ('apiKeys/{apikeyId}'),
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

    def create_apikey(self, api_key_name, api_key_type, environment_ids, workspace_id):
        '''
        create new apikey

        :param: apikey info, environment and workaspce

        :returns: APIKey object
        :rtype: APIKey
        '''
        data = {'name':api_key_name,'apiKeyType':api_key_type}
        if environment_ids is not None:
            environmentIds = []
            for env in environment_ids:
                environmentIds.append({'type':'environment', 'id': env})
            data['environments'] = environmentIds
        if workspace_id is not None:
            data['workspace'] = {'type':'workspace', 'id': workspace_id}
        response = self._http_client.make_request(
            self._endpoint['create_apikey'],
            body = data
        )
        return APIKey(response)

    def delete_apikey(self, apikey_id):
        '''
        delete a APIKey

        :param: apikey id

        :returns: True if successful
        :rtype: Boolean
        '''
        response = self._http_client.make_request(
            self._endpoint['delete_apikey'],
            apikeyId = apikey_id
        )
        return True
