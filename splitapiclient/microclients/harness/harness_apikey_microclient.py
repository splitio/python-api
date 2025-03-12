from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import HarnessApiKey
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class HarnessApiKeyMicroClient:
    '''
    Microclient for managing Harness API keys
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'harness/apikeys',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_apikey': {
            'method': 'GET',
            'url_template': 'harness/apikeys/{apikeyId}',
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
            'url_template': 'harness/apikeys',
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
            'url_template': 'harness/apikeys/{apikeyId}',
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
            'url_template': 'harness/apikeys/{apikeyId}',
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
        Returns a list of HarnessApiKey objects.

        :returns: list of HarnessApiKey objects
        :rtype: list(HarnessApiKey)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items']
        )
        return [HarnessApiKey(item, self._http_client) for item in response.get('items', [])]

    def get(self, apikey_id):
        '''
        Get a specific API key by ID

        :param apikey_id: ID of the API key to retrieve
        :returns: HarnessApiKey object
        :rtype: HarnessApiKey
        '''
        response = self._http_client.make_request(
            self._endpoint['get_apikey'],
            apikeyId=apikey_id
        )
        return HarnessApiKey(response, self._http_client)

    def create(self, apikey_data):
        '''
        Create a new API key

        :param apikey_data: Dictionary containing API key data
        :returns: newly created API key
        :rtype: HarnessApiKey
        '''
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=apikey_data
        )
        return HarnessApiKey(response, self._http_client)

    def update(self, apikey_id, update_data):
        '''
        Update an API key

        :param apikey_id: ID of the API key to update
        :param update_data: Dictionary containing update data
        :returns: updated API key
        :rtype: HarnessApiKey
        '''
        response = self._http_client.make_request(
            self._endpoint['update'],
            body=update_data,
            apikeyId=apikey_id
        )
        return HarnessApiKey(response, self._http_client)

    def delete(self, apikey_id):
        '''
        Delete an API key

        :param apikey_id: ID of the API key to delete
        :returns: True if successful
        :rtype: bool
        '''
        self._http_client.make_request(
            self._endpoint['delete'],
            apikeyId=apikey_id
        )
        return True
