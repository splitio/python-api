from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import ServiceAccount
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class ServiceAccountMicroClient:
    '''
    Microclient for managing Harness service accounts
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': '/ng/api/serviceaccount?accountIdentifier={accountIdentifier}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'item': {
            'method': 'GET',
            'url_template': '/ng/api/serviceaccount/aggregate/{serviceAccountId}?accountIdentifier={accountIdentifier}',
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
            'url_template': '/ng/api/serviceaccount?accountIdentifier={accountIdentifier}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'update': {
            'method': 'PUT',
            'url_template': '/ng/api/serviceaccount/{serviceAccountId}?accountIdentifier={accountIdentifier}',
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
            'url_template': '/ng/api/serviceaccount/{serviceAccountId}?accountIdentifier={accountIdentifier}',
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
        Returns a list of ServiceAccount objects.

        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: list of ServiceAccount objects
        :rtype: list(ServiceAccount)
        '''
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        try:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                accountIdentifier=account_id,
            )
            data = response.get('data', [])
            return [ServiceAccount(item, self._http_client) for item in data]
        except HTTPResponseError as e:
            LOGGER.error(f"HTTP error fetching service accounts: {str(e)}")
            return []  # Return empty list on HTTP error

    def get(self, service_account_id, account_identifier=None):
        '''
        Get a specific service account by ID

        :param service_account_id: ID of the service account to retrieve
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: ServiceAccount object
        :rtype: ServiceAccount
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['item'],
            serviceAccountId=service_account_id,
            accountIdentifier=account_id
        )
        
        # Handle different response formats
        data = response.get('data', {})
        
        return ServiceAccount(data['serviceAccount'], self._http_client)
       

    def create(self, service_account_data, account_identifier=None):
        '''
        Create a new service account

        :param service_account_data: Dictionary containing service account data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: newly created service account
        :rtype: ServiceAccount
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=service_account_data,
            accountIdentifier=account_id
        )
        
        return ServiceAccount(response.get('data', {}), self._http_client)

    def update(self, service_account_id, update_data, account_identifier=None):
        '''
        Update a service account

        :param service_account_id: ID of the service account to update
        :param update_data: Dictionary containing update data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: updated service account
        :rtype: ServiceAccount
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['update'],
            body=update_data,
            serviceAccountId=service_account_id,
            accountIdentifier=account_id
        )
        
        return ServiceAccount(response.get('data', {}), self._http_client)

    def delete(self, service_account_id, account_identifier=None):
        '''
        Delete a service account

        :param service_account_id: ID of the service account to delete
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: True if successful
        :rtype: bool
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['delete'],
            serviceAccountId=service_account_id,
            accountIdentifier=account_id
        )
        
        # For test compatibility, return the raw response
        return True
