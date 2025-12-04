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
            'url_template': '/ng/api/user/aggregate?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}&pageIndex={pageIndex}',
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
            'url_template': '/ng/api/user/aggregate/{userId}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/ng/api/user/users?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/ng/api/user/{userId}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/ng/api/user/add-user-to-groups/{userId}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/ng/api/invites/{inviteId}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/ng/api/invites/aggregate?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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

    def list(self, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Returns a list of HarnessUser objects.

        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: list of HarnessUser objects
        :rtype: list(HarnessUser)
        '''
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        page_index = 0
        final_list = []
        while True:
            try:
                # Conditionally modify endpoint URL template to omit optional parameters if not provided
                endpoint = self._endpoint['all_items'].copy()
                if org_id is None:
                    endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
                if project_id is None:
                    endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
                
                request_kwargs = {
                    'pageIndex': page_index,
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
                content = response.get('data', {}).get('content', [])
                if not content:
                    break
                
                final_list.extend([HarnessUser(item['user'], self._http_client) for item in content])
                page_index += 1
            except HTTPResponseError:
                # Break out of the loop if there's an HTTP error with the request
                break
            
        return final_list

    def get(self, user_id, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Get a specific user by ID

        :param user_id: ID of the user to retrieve
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: HarnessUser object
        :rtype: HarnessUser
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['get_user'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        request_kwargs = {
            'userId': user_id,
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
        return HarnessUser(response['data']['user'], self._http_client)

    def invite(self, user_data, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Invite a new user

        :param user_data: Dictionary containing user data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: newly invited user
        :rtype: HarnessUser
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['invite'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        request_kwargs = {
            'body': user_data,
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
        return True

    def update(self, user_id, update_data, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Update a user

        :param user_id: ID of the user to update
        :param update_data: Dictionary containing update data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: updated user
        :rtype: HarnessUser
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['update'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        request_kwargs = {
            'body': update_data,
            'userId': user_id,
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
        return HarnessUser(response.get('data', {}), self._http_client)

    def add_user_to_groups(self, user_id, group_ids, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Add a user to groups

        :param user_id: ID of the user to add to groups
        :param group_ids: List of group IDs to add the user to
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
        endpoint = self._endpoint['add_user_to_groups'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        request_kwargs = {
            'body': {"userGroupIdsToAdd": group_ids},
            'userId': user_id,
            'accountIdentifier': account_id
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

    def delete_pending(self, invite_id, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Delete a pending invite

        :param invite_id: ID of the invite to delete
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
        endpoint = self._endpoint['delete_pending'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        request_kwargs = {
            'inviteId': invite_id,
            'accountIdentifier': account_id
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

    def list_pending(self, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Returns a list of pending users.

        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: list of pending users
        :rtype: list(HarnessUser)
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        page_index = 0
        final_list = []
        while True:
            # Conditionally modify endpoint URL template to omit optional parameters if not provided
            endpoint = self._endpoint['list_pending'].copy()
            if org_id is None:
                endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
            if project_id is None:
                endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
            
            request_kwargs = {
                'pageIndex': page_index,
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
            content = response.get('data', {}).get('content', [])
            if not content:
                break
            
            final_list.extend([HarnessInvite(item, self._http_client) for item in content])
            page_index += 1
            
        return final_list
