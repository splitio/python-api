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
            'url_template': '/ng/api/token/aggregate?apiKeyType=SERVICE_ACCOUNT&accountIdentifier={accountIdentifier}&pageIndex={pageIndex}&pageSize=100',
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
            'url_template': '/ng/api/token?accountIdentifier={accountIdentifier}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'rotate_token': {
            'method': 'POST',
            'url_template': '/ng/api/token/rotate/{tokenId}?accountIdentifier={accountIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}&apiKeyIdentifier={apiKeyIdentifier}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'update_token': {
            'method': 'PUT',
            'url_template': '/ng/api/token/{tokenId}?accountIdentifier={accountIdentifier}',
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
            'url_template': '/ng/api/token/{tokenId}?accountIdentifier={accountIdentifier}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
    }

    def __init__(self, http_client, account_identifier=None):
        '''
        Constructor

        :param http_client: HTTP client to use for requests
        :param account_identifier: Default account identifier to use for all requests
        '''
        self._http_client = http_client
        self._account_identifier = account_identifier

    def list(self, account_identifier=None):
        '''
        Returns a list of Token objects.

        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: list of Token objects
        :rtype: list(Token)
        '''
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        
        page_index = 0
        final_list = []
        while True:
            try:
                response = self._http_client.make_request(
                    self._endpoint['all_items'],
                    accountIdentifier=account_id,
                    pageIndex=page_index
                )
                data = response.get('data', {})
                
                content = data.get('content', [])
                if content:
                    # Extract token data from each item in the list
                    for item in content:
                        if isinstance(item, dict) and 'token' in item:
                            final_list.append(item['token'])
                else:
                    break
                    
                page_index += 1
            except HTTPResponseError:
                # Break out of the loop if there's an HTTP error with the request
                break
        
        return [Token(item, self._http_client) for item in final_list]

    def get(self, token_id, account_identifier=None):
        '''
        Get a specific token by ID

        :param token_id: ID of the token to retrieve
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: Token object
        :rtype: Token
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        tokens = self.list(account_identifier=account_id)
        # Since tokens is already a list of Token objects, we need to check the _identifier attribute
        return next((token for token in tokens if token._identifier == token_id), None)

    def create(self, token_data, account_identifier=None):
        '''
        Create a new token

        :param token_data: Dictionary containing token data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: newly created token
        :rtype: Token
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=token_data,
            accountIdentifier=account_id
        )
        return response.get('data', "")

    def update(self, token_id, update_data, account_identifier=None):
        '''
        Update a token

        :param token_id: ID of the token to update
        :param update_data: Dictionary containing update data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: updated token
        :rtype: Token
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['update_token'],
            body=update_data,
            tokenId=token_id,
            accountIdentifier=account_id
        )
        return Token(response.get('data', {}), self._http_client)


    def rotate(self, token_id, parent_identifier, api_key_identifier, account_identifier=None):
        '''
        Rotate a token

        :param token_id: ID of the token to rotate
        :param parent_identifier: Parent identifier for the token
        :param api_key_identifier: API key identifier for the token
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: rotated token
        :rtype: string
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['rotate_token'],
            tokenId=token_id,
            parentIdentifier=parent_identifier,
            apiKeyIdentifier=api_key_identifier,
            accountIdentifier=account_id
        )
        return response.get('data', "")

    def delete(self, token_id, account_identifier=None):
        '''
        Delete a token

        :param token_id: ID of the token to delete
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: True if successful
        :rtype: bool
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        self._http_client.make_request(
            self._endpoint['delete'],
            tokenId=token_id,
            accountIdentifier=account_id
        )
        return True
