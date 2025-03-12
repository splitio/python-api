from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import Token
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class TokenMicroClient:
    '''
    Microclient for managing Harness tokens
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'tokens',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_token': {
            'method': 'GET',
            'url_template': 'tokens/{tokenId}',
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
            'url_template': 'tokens',
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
            'url_template': 'tokens/{tokenId}',
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
        Returns a list of Token objects.

        :returns: list of Token objects
        :rtype: list(Token)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items']
        )
        return [Token(item, self._http_client) for item in response.get('items', [])]

    def get(self, token_id):
        '''
        Get a specific token by ID

        :param token_id: ID of the token to retrieve
        :returns: Token object
        :rtype: Token
        '''
        response = self._http_client.make_request(
            self._endpoint['get_token'],
            tokenId=token_id
        )
        return Token(response, self._http_client)

    def create(self, token_data):
        '''
        Create a new token

        :param token_data: Dictionary containing token data
        :returns: newly created token
        :rtype: Token
        '''
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=token_data
        )
        return Token(response, self._http_client)

    def delete(self, token_id):
        '''
        Delete a token

        :param token_id: ID of the token to delete
        :returns: True if successful
        :rtype: bool
        '''
        self._http_client.make_request(
            self._endpoint['delete'],
            tokenId=token_id
        )
        return True
