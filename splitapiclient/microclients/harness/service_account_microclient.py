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
            'url_template': 'serviceAccounts',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_service_account': {
            'method': 'GET',
            'url_template': 'serviceAccounts/{serviceAccountId}',
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
            'url_template': 'serviceAccounts',
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
            'url_template': 'serviceAccounts/{serviceAccountId}',
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
            'url_template': 'serviceAccounts/{serviceAccountId}',
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
        Returns a list of ServiceAccount objects.

        :returns: list of ServiceAccount objects
        :rtype: list(ServiceAccount)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items']
        )
        return [ServiceAccount(item, self._http_client) for item in response.get('items', [])]

    def get(self, service_account_id):
        '''
        Get a specific service account by ID

        :param service_account_id: ID of the service account to retrieve
        :returns: ServiceAccount object
        :rtype: ServiceAccount
        '''
        response = self._http_client.make_request(
            self._endpoint['get_service_account'],
            serviceAccountId=service_account_id
        )
        return ServiceAccount(response, self._http_client)

    def create(self, service_account_data):
        '''
        Create a new service account

        :param service_account_data: Dictionary containing service account data
        :returns: newly created service account
        :rtype: ServiceAccount
        '''
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=service_account_data
        )
        return ServiceAccount(response, self._http_client)

    def update(self, service_account_id, update_data):
        '''
        Update a service account

        :param service_account_id: ID of the service account to update
        :param update_data: Dictionary containing update data
        :returns: updated service account
        :rtype: ServiceAccount
        '''
        response = self._http_client.make_request(
            self._endpoint['update'],
            body=update_data,
            serviceAccountId=service_account_id
        )
        return ServiceAccount(response, self._http_client)

    def delete(self, service_account_id):
        '''
        Delete a service account

        :param service_account_id: ID of the service account to delete
        :returns: True if successful
        :rtype: bool
        '''
        self._http_client.make_request(
            self._endpoint['delete'],
            serviceAccountId=service_account_id
        )
        return True
