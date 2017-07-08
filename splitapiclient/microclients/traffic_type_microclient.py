from splitapiclient.resources import TrafficType
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER


class TrafficTypeMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'trafficTypes',
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

    def list(self):
        '''
        Returns a list of TrafficType objects.

        :returns: List of TrafficType objects
        :rtype: list(TrafficType)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items']
        )
        return [TrafficType(item, self._http_client) for item in response]
