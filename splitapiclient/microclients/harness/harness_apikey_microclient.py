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
            'url_template': '/ng/api/apikey?accountIdentifier={accountIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}',
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
            'url_template': '/ng/api/apikey/aggregate/{apiKeyIdentifier}?accountIdentifier={accountIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}',
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
            'url_template': '/ng/api/apikey?accountIdentifier={accountIdentifier}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'add_permissions': {
            'method': 'POST',
            'url_template': '/ng/api/roleassignments?accountIdentifier={accountIdentifier}',
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
            'url_template': '/ng/api/apikey/{apiKeyIdentifier}?accountIdentifier={accountIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}',
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

    def list(self, parent_identifier=None, account_identifier=None):
        '''
        Returns a list of HarnessApiKey objects.

        :param parent_identifier: Parent identifier for the API keys
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: list of HarnessApiKey objects
        :rtype: list(HarnessApiKey)
        '''
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        try:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                accountIdentifier=account_id,
                parentIdentifier=parent_identifier or ""
            )
            LOGGER.debug('Response: %s', response)
            return [HarnessApiKey(item, self._http_client) for item in response.get('data', [])]
        except HTTPResponseError as e:
            LOGGER.error(f"HTTP error fetching API keys: {str(e)}")
            return []  # Return empty list on HTTP error

    def get(self, apikey_id, parent_identifier=None, account_identifier=None):
        '''
        Get a specific API key by ID

        :param apikey_id: ID of the API key to retrieve
        :param parent_identifier: Parent identifier for the API key
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: HarnessApiKey object
        :rtype: HarnessApiKey
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['get_apikey'],
            apiKeyIdentifier=apikey_id,
            accountIdentifier=account_id,
            parentIdentifier=parent_identifier or ""
        )
        LOGGER.debug('Response: %s', response)
        if(response.get('data').get('apiKey')):
            return HarnessApiKey(response.get('data').get('apiKey'), self._http_client)
        return None

    def create(self, apikey_data, account_identifier=None):
        '''
        Create a new API key

        :param apikey_data: Dictionary containing API key data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: newly created API key
        :rtype: HarnessApiKey
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=apikey_data,
            accountIdentifier=account_id
        )
        LOGGER.debug('Response: %s', response)
        if(response.get('data')):
            return HarnessApiKey(response.get('data'), self._http_client)
        return None


    def add_permissions(self, apikey_id, permissions, account_identifier=None):
        '''
        Add permissions to an API key

        :param apikey_id: ID of the API key to add permissions to
        :param permissions: List of permissions to add as a role assignment
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: True if successful
        :rtype: bool
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['add_permissions'],
            body=permissions,
            apiKeyIdentifier=apikey_id,
            accountIdentifier=account_id
        )
        LOGGER.debug('Response: %s', response)
        return True

    def delete(self, apikey_id, parent_identifier=None, account_identifier=None):
        '''
        Delete an API key

        :param apikey_id: ID of the API key to delete
        :param parent_identifier: Parent identifier for the API key
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
            apiKeyIdentifier=apikey_id,
            accountIdentifier=account_id,
            parentIdentifier=parent_identifier or ""
        )
        return True
