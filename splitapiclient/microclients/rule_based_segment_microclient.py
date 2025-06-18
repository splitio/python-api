from splitapiclient.resources import RuleBasedSegment
from splitapiclient.resources import RuleBasedSegmentDefinition
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class RuleBasedSegmentMicroClient:
    '''
    MicroClient for rule-based segments
    '''
    _endpoint = {
        'create': {
            'method': 'POST',
            'url_template': ('rule-based-segments/ws/{workspaceId}/trafficTypes/{trafficTypeName}'),
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
            'url_template': ('rule-based-segments/{environmentId}/{segmentName}'),
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
            'url_template': ('rule-based-segments/{environmentId}/{segmentName}'),
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
            'url_template': ('rule-based-segments/ws/{workspaceId}/{segmentName}'),
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
            'url_template': 'rule-based-segments/ws/{workspaceId}?limit={limit}&offset={offset}',
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

    def list(self, workspace_id, offset=0, limit=50):
        '''
        Returns a list of RuleBasedSegment objects with pagination support.

        :param workspace_id: id of the workspace
        :param offset: starting position for pagination (default: 0)
        :param limit: maximum number of items to return (default: 50)
        :returns: list of RuleBasedSegment objects
        :rtype: list(RuleBasedSegment)
        '''
        segment_list = []
        current_offset = offset
        
        while True:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                workspaceId = workspace_id,
                offset = current_offset,
                limit = limit
            )
            
            # Process the current page of results
            current_page_items = []
            if isinstance(response, list):
                for item in response:
                    current_page_items.append(RuleBasedSegment(item, self._http_client))
            
            # Add current page items to the full list
            segment_list.extend(current_page_items)
            
            # If we reached the end (fewer items than limit), then break the loop
            # or if we have more than limit items, then the pagination logic isn't implemented yet at the api
            if len(current_page_items) < limit or len(current_page_items) > limit:
                break
                
            # Otherwise move to the next page
            current_offset += limit
            
        return segment_list

    def find(self, segment_name, workspace_id):
        '''
        Find RuleBasedSegment in environment list objects.

        :returns: RuleBasedSegment objects
        :rtype: RuleBasedSegment
        '''
        for item in self.list(workspace_id):
            if item.name == segment_name:
                return item
        LOGGER.error("RuleBasedSegment Name does not exist")
        return None

    def add(self, segment, traffic_type_name, workspace_id):
        '''
        add a rule-based segment

        :param segment: rule-based segment instance or dict
        
        :returns: newly created rule-based segment
        :rtype: RuleBasedSegment
        '''
        data = as_dict(segment)
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=data,
            workspaceId = workspace_id,
            trafficTypeName = traffic_type_name
        )
        response['workspaceId'] = workspace_id
        return RuleBasedSegment(response, self._http_client)

    def delete(self, segment_name, workspace_id):
        '''
        delete a rule-based segment

        :param segment: rule-based segment instance or dict

        :returns:
        :rtype: RuleBasedSegment
        '''
        response = self._http_client.make_request(
            self._endpoint['delete'],
            workspaceId = workspace_id,
            segmentName = segment_name
        )
        return response

    def add_to_environment(self, segment_name, environment_id, workspace_id=None):
        '''
        add a rule-based segment to environment

        :param segment_name: name of the rule-based segment
        :param environment_id: id of the environment
        :param workspace_id: id of the workspace (optional)
        
        :returns: newly created rule-based segment definition object
        :rtype: RuleBasedSegmentDefinition
        '''
        response = self._http_client.make_request(
            self._endpoint['add_to_environment'],
            body="",
            segmentName = segment_name,
            environmentId = environment_id,

        )
        return RuleBasedSegmentDefinition(response, self._http_client, workspace_id)

    def remove_from_environment(self, segment_name, environment_id):
        '''
        remove a rule-based segment from environment

        :param segment: rule-based segment name, environment id
        
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
