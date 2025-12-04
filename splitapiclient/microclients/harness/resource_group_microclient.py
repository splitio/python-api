from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import ResourceGroup
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class ResourceGroupMicroClient:
    '''
    Microclient for managing Harness resource groups
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': '/resourcegroup/api/v2/resourcegroup?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}&pageIndex={pageIndex}&pageSize=100',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_resource_group': {
            'method': 'GET',
            'url_template': '/resourcegroup/api/v2/resourcegroup/{resourceGroupId}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/resourcegroup/api/v2/resourcegroup?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/resourcegroup/api/v2/resourcegroup/{resourceGroupId}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
            'url_template': '/resourcegroup/api/v2/resourcegroup/{resourceGroupId}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&projectIdentifier={projectIdentifier}',
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
        Returns a list of ResourceGroup objects.

        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: list of ResourceGroup objects
        :rtype: list(ResourceGroup)
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
                    'accountIdentifier': account_id,
                    'pageIndex': page_index
                }
                if org_id is not None:
                    request_kwargs['orgIdentifier'] = org_id
                if project_id is not None:
                    request_kwargs['projectIdentifier'] = project_id
                    
                response = self._http_client.make_request(
                    endpoint,
                    **request_kwargs
                )
                data = response.get('data', {})
                content_obj = data.get('content', []) if isinstance(data.get('content'), list) else []
                content = []
                for item in content_obj:
                    if isinstance(item, dict) and 'resourceGroup' in item:
                        content.append(item['resourceGroup'])
                
                final_list.extend(content)
                if not content:
                    break
                page_index += 1
            except HTTPResponseError:
                # Break out of the loop if there's an HTTP error with the request
                break
            
        return [ResourceGroup(item, self._http_client) for item in final_list]

    def get(self, resource_group_id, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Get a specific resource group by ID

        :param resource_group_id: ID of the resource group to retrieve
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: ResourceGroup object
        :rtype: ResourceGroup
        '''
        # Use the provided account_identifier or fall back to the default
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
        project_id = project_identifier if project_identifier is not None else self._project_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['get_resource_group'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        if project_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&projectIdentifier={projectIdentifier}', '')
        
        request_kwargs = {
            'resourceGroupId': resource_group_id,
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
        return ResourceGroup(response.get('data', {}).get('resourceGroup', {}), self._http_client)

    def create(self, resource_group_data, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Create a new resource group

        :param resource_group_data: Dictionary containing resource group data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: newly created resource group
        :rtype: ResourceGroup
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
            'body': resource_group_data,
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
        resourceGroup = response.get('data', {}).get('resourceGroup', {})
        return ResourceGroup(resourceGroup, self._http_client)

    def update(self, resource_group_id, update_data, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Update a resource group

        :param resource_group_id: ID of the resource group to update
        :param update_data: Dictionary containing update data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :param project_identifier: Project identifier to use for this request, overrides the default
        :returns: updated resource group
        :rtype: ResourceGroup
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
            'resourceGroupId': resource_group_id,
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
        resourceGroup = response.get('data', {}).get('resourceGroup', {})
        return ResourceGroup(resourceGroup, self._http_client)

    def delete(self, resource_group_id, account_identifier=None, org_identifier=None, project_identifier=None):
        '''
        Delete a resource group

        :param resource_group_id: ID of the resource group to delete
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
            'resourceGroupId': resource_group_id,
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
