from splitapiclient.resources import RuleBasedSegmentDefinition
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class RuleBasedSegmentDefinitionMicroClient:
    '''
    MicroClient for rule-based segment definitions
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'rule-based-segments/ws/{workspaceId}/environments/{environmentId}?offset={offset}&limit={limit}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'update': {
            'method': 'PUT',
            'url_template': 'rule-based-segments/ws/{workspaceId}/{segmentName}/environments/{environmentId}',
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
            'url_template': 'rule-based-segments/{environmentId}/{segmentName}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        }
    }

    def __init__(self, http_client):
        '''
        Constructor
        '''
        self._http_client = http_client

    def list(self, environment_id, workspace_id, offset=0, limit=50):
        '''
        Returns a list of RuleBasedSegment in environment objects with pagination support.

        :param environment_id: id of the environment
        :param workspace_id: id of the workspace
        :param offset: starting position for pagination (default: 0)
        :param limit: maximum number of items to return (default: 50)
        :param fetch_all: if True, fetches all pages and returns a consolidated list
        :returns: list of RuleBasedSegment in environment objects
        :rtype: list(RuleBasedSegmentDefinition)
        '''
        segment_definition_list = []
        current_offset = offset
        
        while True:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                workspaceId = workspace_id,
                environmentId = environment_id,
                offset = current_offset,
                limit = limit
            )
            
            # Process the current page of results
            current_page_items = []
            if isinstance(response, list):
                for item in response:
                    item['environment'] = {'id':environment_id, 'name':''}
                    current_page_items.append(RuleBasedSegmentDefinition(item, self._http_client, workspace_id=workspace_id))
            
            # Add current page items to the full list
            segment_definition_list.extend(current_page_items)
            
            # If we reached the end
            # (fewer items than limit), then break the loop
            # or if we have more than limit items, then the pagination logic isn't implemented yet at the api
            if len(current_page_items) < limit or len(current_page_items) > limit:
                break
                
            # Otherwise move to the next page
            current_offset += limit
            
        return segment_definition_list

    def find(self, segment_name, environment_id, workspace_id):
        '''
        Find RuleBasedSegment in environment list objects.

        :param segment_name: name of the rule-based segment to find
        :param environment_id: id of the environment
        :param workspace_id: id of the workspace
        :returns: RuleBasedSegmentDefinition object
        :rtype: RuleBasedSegmentDefinition
        '''
        for item in self.list(environment_id, workspace_id):
            if item.name == segment_name:
                return item
        LOGGER.error("RuleBasedSegment Definition Name does not exist")
        return None

    def update(self, segment_name, environment_id, workspace_id, data):
        '''
        Update RuleBasedSegmentDefinition object.

        :param segment_name: name of the rule-based segment
        :param environment_id: id of the environment
        :param workspace_id: id of the workspace
        :param data: dictionary of data to update

        :returns: RuleBasedSegmentDefinition object
        :rtype: RuleBasedSegmentDefinition
        '''
        response = self._http_client.make_request(
            self._endpoint['update'],
            body=as_dict(data),
            workspaceId = workspace_id,
            environmentId = environment_id,
            segmentName = segment_name
        )
        return RuleBasedSegmentDefinition(as_dict(response), self._http_client)

    def delete(self, segment_name, environment_id):
        '''
        Delete RuleBasedSegmentDefinition object.

        :param segment_name: name of the rule-based segment
        :param environment_id: id of the environment

        :returns: True if successful
        :rtype: boolean
        '''
        self._http_client.make_request(
            self._endpoint['delete'],
            environmentId = environment_id,
            segmentName = segment_name
        )
        return True
