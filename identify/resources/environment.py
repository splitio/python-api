from identify.resources.base_resource import BaseResource
from identify.util.logger import LOGGER


class Environment(BaseResource):
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'environments',
            'url_parameters': [],
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True
        }
    }

    _schema = {
        'id': 'string',
        'name': 'string',
    }

    def __init__(self, client, id, name):
        '''
        '''
        BaseResource.__init__(self, client, id)
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @classmethod
    def _build_single_from_collection_response(cls, client, response):
        '''
        '''
        return Environment(
            client,
            response['id'],
            response['name']
        )
