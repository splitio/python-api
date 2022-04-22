from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.resources import TrafficType


class TrafficTypeMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'trafficTypes/ws/{workspaceId}',
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
            'url_template': ('trafficTypes/{trafficTypeId}'),
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
        Returns a list of TrafficType objects.

        :returns: List of TrafficType objects
        :rtype: list(TrafficType)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items'],
            workspaceId = workspace_id
        )
        return [TrafficType(item, self._http_client) for item in response]

    def find(self, traffic_type_name, workspace_id):
        '''
        Find TrafficType in workspace

        :returns: TrafficType object
        :rtype: TrafficType
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items'],
            workspaceId = workspace_id
        )
        for item in response:
            if item['name']==traffic_type_name:
                return TrafficType(item, workspace_id, self._http_client)
        LOGGER.error("TrafficType Name does not exist")
        return None

    def delete(self, traffic_type_id):
        '''
        delete a traffic type

        :param traffic type id:

        :returns:
        :rtype: True if successful
        '''
        response = self._http_client.make_request(
            self._endpoint['delete'],
            trafficTypeId = traffic_type_id,
        )
        return response
