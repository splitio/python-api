from identify.resources.traffic_type import TrafficType
from identify.util.exceptions import HTTPResponseError, \
    UnknownIdentifyClientError
from identify.util.logger import LOGGER


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
#        'fetch_attributes': Attribute._endpoint['all_items'],
#        'add_attribute': Attribute._endpoint['create']
    }

    def __init__(self, http_client):
        '''
        '''
        self._http_client = http_client

    def list(self):
        '''
        Returns a list of TrafficType objects.
        '''
        try:
            response = self._http_client.make_request(
                self._endpoint['all_items']
            )
            return [TrafficType(item) for item in response]
        except HTTPResponseError as e:
            LOGGER.error('Error retrieving items')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()
