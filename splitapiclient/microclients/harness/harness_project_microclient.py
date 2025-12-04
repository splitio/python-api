from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.harness import HarnessProject
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict


class HarnessProjectMicroClient:
    '''
    Microclient for managing Harness projects
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': '/ng/api/projects?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}&pageIndex={pageIndex}&pageSize=50',
            'headers': [{
                'name': 'x-api-key',
                'template': '{value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get': {
            'method': 'GET',
            'url_template': '/ng/api/projects/{projectIdentifier}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}',
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
            'url_template': '/ng/api/projects?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}',
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
            'url_template': '/ng/api/projects/{projectIdentifier}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}',
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
            'url_template': '/ng/api/projects/{projectIdentifier}?accountIdentifier={accountIdentifier}&orgIdentifier={orgIdentifier}',
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

    def list(self, account_identifier=None, org_identifier=None):
        '''
        Returns a list of HarnessProject objects.

        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :returns: list of HarnessProject objects
        :rtype: list(HarnessProject)
        '''
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
            
        page_index = 0
        final_list = []
        last_json = None
        total_projects_seen = 0
        while True:
            try:
                # Conditionally modify endpoint URL template to omit optional parameters if not provided
                endpoint = self._endpoint['all_items'].copy()
                if org_id is None:
                    endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
                
                request_kwargs = {
                    'pageIndex': page_index,
                    'accountIdentifier': account_id
                }
                if org_id is not None:
                    request_kwargs['orgIdentifier'] = org_id
                    
                response = self._http_client.make_request(
                    endpoint,
                    **request_kwargs
                )

                data = response.get('data', {})
                
                # Convert to JSON string for deep comparison
                import json
                current_json = json.dumps(data, sort_keys=True)
                
                # If we get the same response twice, we're in a loop
                if current_json == last_json:
                    break
                
                last_json = current_json

                content_obj = data.get('content', []) if isinstance(data.get('content'), list) else []
                content = []
                for item in content_obj:
                    if isinstance(item, dict) and 'project' in item:
                        content.append(item['project'])
                
                # Also break if we get empty content
                if not content:
                    break

                final_list.extend(content)
                total_projects_seen += len(content)
                
               
                # Get pagination info if available
                total_elements = data.get('totalElements', 0)
                total_pages = data.get('totalPages', 0)
                if total_elements and total_pages:
                    # If we've seen all pages according to API, break
                    if page_index >= total_pages - 1:  # -1 because pages are 0-indexed
                        break
                
                page_index += 1

            except HTTPResponseError as e:
                LOGGER.error(f"HTTP error fetching projects: {str(e)}")
                break  # Break the loop on HTTP error
            except Exception as e:
                LOGGER.error(f"Error fetching projects: {str(e)}")
                break  # Break the loop on any other error
            
        return [HarnessProject(item, self._http_client) for item in final_list]

    def get(self, project_identifier, account_identifier=None, org_identifier=None):
        '''
        Get a specific project by ID

        :param project_identifier: ID of the project to retrieve (path parameter)
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :returns: HarnessProject object
        :rtype: HarnessProject
        '''
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['get'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        
        request_kwargs = {
            'projectIdentifier': project_identifier,  # Path parameter - replaces {projectIdentifier} in path
            'accountIdentifier': account_id
        }
        if org_id is not None:
            request_kwargs['orgIdentifier'] = org_id
            
        response = self._http_client.make_request(
            endpoint,
            **request_kwargs
        )
        return HarnessProject(response.get('data', {}).get('project', {}), self._http_client)

    def create(self, project_data, account_identifier=None, org_identifier=None):
        '''
        Create a new project

        :param project_data: Dictionary containing project data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :returns: newly created project
        :rtype: HarnessProject
        '''
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['create'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        
        request_kwargs = {
            'body': project_data,
            'accountIdentifier': account_id
        }
        if org_id is not None:
            request_kwargs['orgIdentifier'] = org_id
            
        response = self._http_client.make_request(
            endpoint,
            **request_kwargs
        )
        return HarnessProject(response.get('data', {}).get('project', {}), self._http_client)

    def update(self, project_identifier, project_data, account_identifier=None, org_identifier=None):
        ''' 
        Update an existing project

        :param project_identifier: ID of the project to update (path parameter)
        :param project_data: Dictionary containing updated project data
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :returns: updated project
        :rtype: HarnessProject
        '''
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['update'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        
        request_kwargs = {
            'projectIdentifier': project_identifier,  # Path parameter - replaces {projectIdentifier} in path
            'accountIdentifier': account_id,
            'body': project_data
        }
        if org_id is not None:
            request_kwargs['orgIdentifier'] = org_id
            
        response = self._http_client.make_request(
            endpoint,
            **request_kwargs
        )
        return HarnessProject(response.get('data', {}).get('project', {}), self._http_client)

    def delete(self, project_identifier, account_identifier=None, org_identifier=None):
        '''
        Delete a project

        :param project_identifier: ID of the project to delete (path parameter)
        :param account_identifier: Account identifier to use for this request, overrides the default
        :param org_identifier: Organization identifier to use for this request, overrides the default
        :returns: True if successful
        :rtype: bool
        '''
        account_id = account_identifier if account_identifier is not None else self._account_identifier
        if account_id is None:
            raise ValueError("account_identifier must be provided either at client initialization or method call")
        org_id = org_identifier if org_identifier is not None else self._org_identifier
            
        # Conditionally modify endpoint URL template to omit optional parameters if not provided
        endpoint = self._endpoint['delete'].copy()
        if org_id is None:
            endpoint['url_template'] = endpoint['url_template'].replace('&orgIdentifier={orgIdentifier}', '')
        
        request_kwargs = {
            'projectIdentifier': project_identifier,  # Path parameter - replaces {projectIdentifier} in path
            'accountIdentifier': account_id
        }
        if org_id is not None:
            request_kwargs['orgIdentifier'] = org_id
            
        self._http_client.make_request(
            endpoint,
            **request_kwargs
        )
        return True
