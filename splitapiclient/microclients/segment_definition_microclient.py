from splitapiclient.resources import SegmentDefinition
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class SegmentDefinitionMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'segments/ws/{workspaceId}/environments/{environmentId}?limit=50&offset={offset}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_keys': {
            'method': 'GET',
            'url_template': 'segments/{environmentId}/{segmentName}/keys?limit=100&offset={offset}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'import_from_json': {
            'method': 'PUT',
            'url_template': 'segments/{environmentId}/{segmentName}/uploadKeys?replace={replaceKeys}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'remove_keys': {
            'method': 'PUT',
            'url_template': 'segments/{environmentId}/{segmentName}/removeKeys',
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

    def list(self, environment_id, workspace_id):
        '''
        Returns a list of Segment in environemnt objects.

        :returns: list of Segment in environemnt objects
        :rtype: list(SegmentDefinition)
        '''
        offset_val = 0
        final_list = []
        while True:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                workspaceId = workspace_id,
                environmentId = environment_id,
                offset = offset_val
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
        segment_definition_list = []
        for item in final_list:
            item['environment'] = {'id':environment_id, 'name':''}
            segment_definition_list.append(SegmentDefinition(item, self._http_client))
        return segment_definition_list

    def find(self, segment_name, environment_id, workspace_id):
        '''
        Find Segment in environment list objects.

        :returns: SegmentDefinition object
        :rtype: SegmentDefinition
        '''
        for item in self.list(environment_id, workspace_id):
            if item.name == segment_name:
                return item
        LOGGER.error("Segment Definition Name does not exist")
        return None

    def get_keys(self, segment_name, environment_id):
        '''
        Returns a list of Keys in Segment in environemnt objects.

        :returns: list of keys in Segment in environemnt objects
        :rtype: list(string)
        '''
        offset_val = 0
        final_list = []
        while True:
            response = self._http_client.make_request(
                self._endpoint['get_keys'],
                environmentId = environment_id,
                segmentName = segment_name,
                offset = offset_val
            )
            for item in response['keys']:
                final_list.append(as_dict(item))
            offset = int(response['offset'])
            totalCount = int(response['count'])
            limit = int(response['limit'])
            if totalCount>(offset+limit):
                offset_val = offset_val + limit
                continue
            else:
                break
        return [item["key"] for item in final_list]

    def import_keys_from_json(self, segment_name, environment_id, replace_keys, data):
        '''
        import keys from csv file into segment

        :param segment: segment name, environment id, replace boolean flag, json data
        
        :returns: True
        :rtype: boolean
        '''
        response = self._http_client.make_request(
            self._endpoint['import_from_json'],
            body=as_dict(data),
            environmentId = environment_id,
            segmentName = segment_name,
            replaceKeys = replace_keys
        )
        return True

    def remove_keys(self, segment_name, environment_id, data):
        '''
        remove keys from csv file into segment

        :param segment: segment name, environment id, json data
        
        :returns: True
        :rtype: boolean
        '''
        response = self._http_client.make_request(
            self._endpoint['remove_keys'],
            body=as_dict(data),
            environmentId = environment_id,
            segmentName = segment_name
        )
        return True

