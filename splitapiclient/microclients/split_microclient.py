from splitapiclient.resources import Split
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict
from splitapiclient.resources import SplitDefinition


class SplitMicroClient:
    '''
    '''
    _endpoint = {
        'update_description': {
            'method': 'PUT',
            'url_template': ('splits/ws/{workspaceId}/{splitName}/updateDescription'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'create': {
            'method': 'POST',
            'url_template': ('splits/ws/{workspaceId}/trafficTypes/{trafficTypeName}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'delete': {
            'method': 'DELETE',
            'url_template': ('splits/ws/{workspaceId}/{splitName}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get': {
            'method': 'GET',
            'url_template': ('splits/ws/{workspaceId}/{splitName}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'all_items': {
            'method': 'GET',
            'url_template': 'splits/ws/{workspaceId}?limit=20&offset={offset}{tags}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'add_to_environment': {
            'method': 'POST',
            'url_template': ('splits/ws/{workspaceId}/{splitName}/environments/{environmentId}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'remove_from_environment': {
            'method': 'DELETE',
            'url_template': ('splits/ws/{workspaceId}/{splitName}/environments/{environmentId}?title={title}&comment={comment}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'associate_tags': {
            'method': 'POST',
            'url_template': ('tags/ws/{workspaceId}/object/{splitName}/objecttype/Split'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
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

    def list(self, workspace_id, tags = []):
        '''
        Returns a list of Split objects.

        :returns: list of Split objects
        :rtype: list(Split)
        '''
        offset_val = 0
        final_list = []
        tags_list = ""
        for tag in tags:
            tags_list = tags_list + "&tag=" + tag
        while True:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                workspaceId = workspace_id,
                offset = offset_val,
                tags = tags_list
            )
            for item in response['objects']:
                final_list.append(as_dict(item))
            offset = int(response['offset'])
            totalCount = int(response['totalCount'])
            limit = int(response['limit'])
            if totalCount>(offset+limit):
                offset_val = offset_val + limit
                continue
            else:
                break
        return [Split(item, workspace_id, self._http_client) for item in final_list]

    def find(self, split_name, workspace_id, tags = []):
        '''
        Find Split in workspace objects.

        :returns: Split object
        :rtype: Split
        '''
        for item in self.list(workspace_id, tags):
            if item.name == split_name:
                return item
        LOGGER.error("Split Name does not exist")
        return None

    def get(self, split_name, workspace_id):
        '''
        get a split details

        :param split_name: split name
        :param workspace_id: workspace id

        :returns: split object
        :rtype: Split
        '''
        response = self._http_client.make_request(
            self._endpoint['get'],
            workspaceId = workspace_id,
            splitName = split_name
        )
        response['workspaceId'] = workspace_id
        return Split(response, workspace_id, self._http_client)

    def add(self, split, traffic_type_name, workspace_id):
        '''
        add a split

        :param split: split instance or dict
        
        :returns: newly created split
        :rtype: Split
        '''
        data = as_dict(split)
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=as_dict(data),
            workspaceId = workspace_id,
            trafficTypeName = traffic_type_name
        )
        response['workspaceId'] = workspace_id
        return Split(response, workspace_id, self._http_client)

    def delete(self, split_name, workspace_id):
        '''
        delete an split

        :param split: split instance or dict

        :returns:
        :rtype: Split
        '''
        response = self._http_client.make_request(
            self._endpoint['delete'],
            workspaceId = workspace_id,
            splitName = split_name
        )
        return response

    def update_description(self, split_name, new_description, workspace_id):
        '''
        update a split description

        :param split: split name, new description and workspace id
        
        :returns: updated split
        :rtype: Split
        '''
        
        response = self._http_client.make_request(
            self._endpoint['update_description'],
            body=new_description,
            workspaceId = workspace_id,
            splitName = split_name
        )
        return Split(response, workspace_id, self._http_client)

    def add_to_environment(self, split_name, environment_id, workspace_id, data):
        '''
        Add split to environment

        :param split: split name, environment id, workspace id and definition
        
        :returns: updated splitDefinition
        :rtype: SplitDefinition
        '''
        
        response = self._http_client.make_request(
            self._endpoint['add_to_environment'],
            body=as_dict(data),
            workspaceId = workspace_id,
            environmentId = environment_id,
            splitName = split_name
        )
        return SplitDefinition(response, environment_id, workspace_id, self._http_client)

    def remove_from_environment(self, split_name, environment_id,comment, title, workspace_id ):
        '''
        Remove split from environment

        :param split: split name, environment id, workspace id, comment, title
        
        :returns: True if successful
        :rtype: boolean
        '''
        
        response = self._http_client.make_request(
            self._endpoint['remove_from_environment'],
            workspaceId = workspace_id,
            environmentId = environment_id,
            splitName = split_name,
            comment = comment, 
            title = title
        )
        return response

    def associate_tags(self, split_name, tags, workspace_id):
        '''
        Associate tags with Split

        :param split: split name, tags string array, workspace id
        
        :returns: True is successful
        :rtype: Boolean
        '''
        
        response = self._http_client.make_request(
            self._endpoint['associate_tags'],
            body=tags,
            workspaceId = workspace_id,
            splitName = split_name
        )
        return True
