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
            'url_template': '/ng/api/apikey?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}',
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
            'url_template': '/ng/api/apikey/aggregate/{apiKeyIdentifier}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}',
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
            'url_template': '/ng/api/apikey?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/ng/api/roleassignments?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/ng/api/apikey/{apiKeyIdentifier}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}&apiKeyType=SERVICE_ACCOUNT&parentIdentifier={parentIdentifier}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
    }

    def __init__(self, http_client, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Constructor

        :param http_client: HTTP client to use for requests
        :param account_identifier: Default account identifier to use for all requests
        :param org_identifier: Default organization identifier to use for all requests
        :param project_identifier: Default project identifier to use for all requests
        '''
        self._http_client = http_client
        self._account_identifier = account_identifier
        self._org_identifier = org_identifier
        self._project_identifier = project_identifier

    def list(self, parent_identifier=None, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Returns a list of HarnessApiKey objects.

        :param parent_identifier: Parent identifier for the API keys
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: list of HarnessApiKey objects
        :rtype: list(HarnessApiKey)
        '''
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['all_items'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        try:
            request_kwargs = {
                'accountIdentifier': account_id,
                'parentIdentifier': parent_identifier or ""
            }
            if org_id is not None:
                request_kwargs['orgIdentifier'] = org_id
            if project_id is not None:
                request_kwargs['projectIdentifier'] = project_id
                
            response = self._http_client.make_request(
                endpoint,
                **request_kwargs
            )
            LOGGER.debug('Response: %s', response)
            return [HarnessApiKey(item, self._http_client) for item in response.get('data', [])]
        except HTTPResponseError as e:
            LOGGER.error(f"HTTP error fetching API keys: {str(e)}")
            return []  # Return empty list on HTTP error

    def get(self, apikey_id, parent_identifier=None, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Get a specific API key by ID

        :param apikey_id: ID of the API key to retrieve
        :param parent_identifier: Parent identifier for the API key
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: HarnessApiKey object
        :rtype: HarnessApiKey
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['get_apikey'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        request_kwargs = {
            'apiKeyIdentifier': apikey_id,
            'accountIdentifier': account_id,
            'parentIdentifier': parent_identifier or ""
        }
        if org_id is not None:
            request_kwargs['orgIdentifier'] = org_id
        if project_id is not None:
            request_kwargs['projectIdentifier'] = project_id
            
        response = self._http_client.make_request(
            endpoint,
            **request_kwargs
        )
        LOGGER.debug('Response: %s', response)
        if(response.get('data').get('apiKey')):
            return HarnessApiKey(response.get('data').get('apiKey'), self._http_client)
        return None

    def create(self, apikey_data, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Create a new API key

        :param apikey_data: Dictionary containing API key data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: newly created API key
        :rtype: HarnessApiKey
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['create'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        request_kwargs = {
            'body': apikey_data,
            'accountIdentifier': account_id
        }
        if org_id is not None:
            request_kwargs['orgIdentifier'] = org_id
        if project_id is not None:
            request_kwargs['projectIdentifier'] = project_id
            
        response = self._http_client.make_request(
            endpoint,
            **request_kwargs
        )
        LOGGER.debug('Response: %s', response)
        if(response.get('data')):
            return HarnessApiKey(response.get('data'), self._http_client)
        return None


    def add_permissions(self, apikey_id, permissions, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Add permissions to an API key

        :param apikey_id: ID of the API key to add permissions to
        :param permissions: List of permissions to add as a role assignment
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: True if successful
        :rtype: bool
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['add_permissions'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        request_kwargs = {
            'body': permissions,
            'apiKeyIdentifier': apikey_id,
            'accountIdentifier': account_id
        }
        if org_id is not None:
            request_kwargs['orgIdentifier'] = org_id
        if project_id is not None:
            request_kwargs['projectIdentifier'] = project_id
            
        response = self._http_client.make_request(
            endpoint,
            **request_kwargs
        )
        LOGGER.debug('Response: %s', response)
        return True

    def delete(self, apikey_id, parent_identifier=None, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Delete an API key

        :param apikey_id: ID of the API key to delete
        :param parent_identifier: Parent identifier for the API key
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: True if successful
        :rtype: bool
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['delete'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        request_kwargs = {
            'apiKeyIdentifier': apikey_id,
            'accountIdentifier': account_id,
            'parentIdentifier': parent_identifier or ""
        }
        if org_id is not None:
            request_kwargs['orgIdentifier'] = org_id
        if project_id is not None:
            request_kwargs['projectIdentifier'] = project_id
            
        self._http_client.make_request(
            endpoint,
            **request_kwargs
        )
        return True
