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
            'url_template': 'rule-based-segments/ws/{workspaceId}/environments/{environmentId}?limit=50&offset={offset}',
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
        }
    }

    def __init__(self, http_client):
        '''
        Constructor
        '''
        self._http_client = http_client

    def list(self, environment_id, workspace_id):
        '''
        Returns a list of RuleBasedSegment in environment objects.

        :returns: list of RuleBasedSegment in environment objects
        :rtype: list(RuleBasedSegmentDefinition)
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
            for item in response:
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
            segment_definition_list.append(RuleBasedSegmentDefinition(item, self._http_client))
        return segment_definition_list

    def find(self, segment_name, environment_id, workspace_id):
        '''
        Find RuleBasedSegment in environment list objects.

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


