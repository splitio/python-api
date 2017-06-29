from identify.resources.environment import Environment
from identify.util.exceptions import HTTPResponseError, \
    UnknownIdentifyClientError
from identify.util.logger import LOGGER


class EnvironmentMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'environments',
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
        '''
        self._http_client = http_client

    def list(self):
        '''
        Returns a list of Environment objects.
        '''
        try:
            response = self._http_client.make_request(
                self._endpoint['all_items']
            )
            return [Environment(item, self._http_client) for item in response]
        except HTTPResponseError as e:
            LOGGER.error('Error retrieving items')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()
