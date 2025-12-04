from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import HarnessGroup
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class HarnessGroupMicroClient:
    '''
    Microclient for managing Harness groups
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': '/ng/api/user-groups?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}&pageIndex={pageIndex}&pageSize=100',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_group': {
            'method': 'GET',
            'url_template': '/ng/api/user-groups/{groupIdentifier}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/ng/api/user-groups?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/ng/api/user-groups?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/ng/api/user-groups/{groupIdentifier}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
        Returns a list of HarnessGroup objects.

        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: list of HarnessGroup objects
        :rtype: list(HarnessGroup)
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
                
                final_list.extend(content)
                page_index += 1
            except HTTPResponseError:
                # Break out of the loop if there's an HTTP error with the request
                break
            
        return [HarnessGroup(item, self._http_client) for item in final_list]

    def get(self, group_identifier, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Get a specific group by ID

        :param group_identifier: ID of the group to retrieve
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: HarnessGroup object
        :rtype: HarnessGroup
        '''
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['get_group'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        request_kwargs = {
            'groupIdentifier': group_identifier,
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
        return HarnessGroup(response['data'], self._http_client)

    def create(self, group_data, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Create a new group

        :param group_data: Dictionary containing group data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: newly created group
        :rtype: HarnessGroup
        '''
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
            'body': group_data,
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
        return HarnessGroup(response['data'], self._http_client)

    def update(self, update_data, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Update a group

        :param update_data: Dictionary containing update data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: updated group
        :rtype: HarnessGroup
        '''
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
        return HarnessGroup(response, self._http_client)

    def delete(self, group_identifier, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Delete a group

        :param group_identifier: ID of the group to delete
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: True if successful
        :rtype: bool
        '''
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
            'groupIdentifier': group_identifier,
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
