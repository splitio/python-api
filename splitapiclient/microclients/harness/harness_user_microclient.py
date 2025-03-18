from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import HarnessUser, HarnessInvite
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class HarnessUserMicroClient:
    '''
    Microclient for managing Harness users
    '''
    _endpoint = {
        'all_items': {
            'method': 'POST', # yes this is really a post for getting users
            'url_template': '/ng/api/user/aggregate?accountIdentifier={accountIdentifier}&pageIndex={pageIndex}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_user': {
            'method': 'GET',
            'url_template': '/ng/api/user/aggregate/{userId}?accountIdentifier={accountIdentifier}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'invite': {
            'method': 'POST',
            'url_template': '/ng/api/user/users?accountIdentifier={accountIdentifier}',
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
            'url_template': '/ng/api/user/{userId}?accountIdentifier={accountIdentifier}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'add_user_to_groups': {
            'method': 'PUT',
            'url_template': '/ng/api/user/add-user-to-groups/{userId}?accountIdentifier={accountIdentifier}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'delete_pending': {
            'method': 'DELETE',
            'url_template': '/ng/api/invites/{inviteId}?accountIdentifier={accountIdentifier}',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'list_pending': {
            'method': 'POST', # yes this is also really a POST
            'url_template': '/ng/api/invites/aggregate?accountIdentifier={accountIdentifier}',
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
        Returns a list of HarnessUser objects.

        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: list of HarnessUser objects
        :rtype: list(HarnessUser)
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
                    pageIndex=page_index,
                    accountIdentifier=account_id
                )
                content = response.get('data', {}).get('content', [])
                if not content:
                    break
                
                final_list.extend([HarnessUser(item['user'], self._http_client) for item in content])
                page_index += 1
            except HTTPResponseError:
                # Break out of the loop if there's an HTTP error with the request
                break
            
        return final_list

    def get(self, user_id, account_identifier=None):
        '''
        Get a specific user by ID

        :param user_id: ID of the user to retrieve
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: HarnessUser object
        :rtype: HarnessUser
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['get_user'],
            userId=user_id,
            accountIdentifier=account_id
        )
        return HarnessUser(response, self._http_client)

    def invite(self, user_data, account_identifier=None):
        '''
        Invite a new user

        :param user_data: Dictionary containing user data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: newly invited user
        :rtype: HarnessUser
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['invite'],
            body=user_data,
            accountIdentifier=account_id
        )
        return True

    def update(self, user_id, update_data, account_identifier=None):
        '''
        Update a user

        :param user_id: ID of the user to update
        :param update_data: Dictionary containing update data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: updated user
        :rtype: HarnessUser
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        response = self._http_client.make_request(
            self._endpoint['update'],
            body=update_data,
            userId=user_id,
            accountIdentifier=account_id
        )
        return HarnessUser(response.get('data', {}), self._http_client)

    def add_user_to_groups(self, user_id, group_ids, account_identifier=None):
        '''
        Add a user to groups

        :param user_id: ID of the user to add to groups
        :param group_ids: List of group IDs to add the user to
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: True if successful
        :rtype: bool
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        self._http_client.make_request(
            self._endpoint['add_user_to_groups'],
            body={"userGroupIdsToAdd": group_ids},
            userId=user_id,
            accountIdentifier=account_id
        )
        return True

    def delete_pending(self, invite_id, account_identifier=None):
        '''
        Delete a pending invite

        :param invite_id: ID of the invite to delete
        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: True if successful
        :rtype: bool
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        self._http_client.make_request(
            self._endpoint['delete_pending'],
            inviteId=invite_id,
            accountIdentifier=account_id
        )
        return True

    def list_pending(self, account_identifier=None):
        '''
        Returns a list of pending users.

        :param account_identifier: Account identifier to use for this request, overrides the default
        :returns: list of pending users
        :rtype: list(HarnessUser)
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
            
        page_index = 0
        final_list = []
        while True:
            response = self._http_client.make_request(
                self._endpoint['list_pending'],
                pageIndex=page_index,
                accountIdentifier=account_id
            )
            content = response.get('data', {}).get('content', [])
            if not content:
                break
            
            final_list.extend([HarnessInvite(item, self._http_client) for item in content])
            page_index += 1
            
        return final_list
