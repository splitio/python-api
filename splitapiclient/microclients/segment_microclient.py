from splitapiclient.resources import Segment
from splitapiclient.resources import SegmentDefinition
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class SegmentMicroClient:
    '''
    '''
    _endpoint = {
        'create': {
            'method': 'POST',
            'url_template': ('segments/ws/{workspaceId}/trafficTypes/{trafficTypeName}'),
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
            'url_template': ('segments/{environmentId}/{segmentName}'),
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
            'url_template': ('segments/{environmentId}/{segmentName}'),
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
            'url_template': ('segments/ws/{workspaceId}/{segmentName}'),
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
            'url_template': 'segments/ws/{workspaceId}?limit=50&offset={offset}',
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

    def list(self, workspace_id):
        '''
        Returns a list of Segment objects.

        :returns: list of Segment objects
        :rtype: list(Segment)
        '''
        offset_val = 0
        final_list = []
        while True:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                workspaceId = workspace_id,
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
        return [Segment(item, self._http_client) for item in final_list]

    def find(self, segment_name, workspace_id):
        '''
        Find Segment in environment list objects.

        :returns: Segment objects
        :rtype: Segment
        '''
        for item in self.list(workspace_id):
            if item.name == segment_name:
                return item
        LOGGER.error("Segment Name does not exist")
        return None

    def add(self, segment, traffic_type_name, workspace_id):
        '''
        add a segment

        :param segment: segment instance or dict
        
        :returns: newly created segment
        :rtype: Segment
        '''
        data = as_dict(segment)
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=data,
            workspaceId = workspace_id,
            trafficTypeName = traffic_type_name
        )
        response['workspaceId'] = workspace_id
        return Segment(response, self._http_client)

    def delete(self, segment_name, workspace_id):
        '''
        delete an segment

        :param segment: segment instance or dict

        :returns:
        :rtype: Segment
        '''
        response = self._http_client.make_request(
            self._endpoint['delete'],
            workspaceId = workspace_id,
            segmentName = segment_name
        )
        return response

    def add_to_environment(self, segment_name, environment_id):
        '''
        add a segment to environment

        :param segment: segment name, environment id
        
        :returns: newly created segmentDescription object
        :rtype: SegmentDescription
        '''
        response = self._http_client.make_request(
            self._endpoint['add_to_environment'],
            body="",
            segmentName = segment_name,
            environmentId = environment_id
        )
        return SegmentDefinition(response, self._http_client)

    def remove_from_environment(self, segment_name, environment_id):
        '''
        from a segment from environment

        :param segment: segment name, environment id
        
        :returns: http response
        :rtype: boolean
        '''
        response = self._http_client.make_request(
            self._endpoint['remove_from_environment'],
            body="",
            segmentName = segment_name,
            environmentId = environment_id
        )
        return response
