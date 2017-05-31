from identify.resources.base_resource import BaseResource
from identify.resources.attribute import Attribute
from identify.util.logger import LOGGER


class TrafficType(BaseResource):
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
        'fetch_attributes': Attribute._endpoint['all_items'],
        'add_attribute': Attribute._endpoint['create']
    }

    _schema = {
        'id': 'string',
        'name': 'string',
        'displayAttributeId': 'string'
    }

    def __init__(self, client, id, name=None, display_name=None):
        '''
        '''
        BaseResource.__init__(self, client, id)
        self._name = name
        self._display_name = display_name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def display_name(self):
        return self._display_name

    def fetch_attributes(self):
        '''
        '''
        return Attribute.retrieve_all(self._client, trafficTypeId=self._id)

    def add_attribute(self, id, display_name, description, data_type):
        '''
        '''
        return Attribute.create(
            id,
            self._id,
            display_name,
            description,
            data_type
        )

    @classmethod
    def _build_single_from_collection_response(cls, client, response):
        '''
        '''
        return TrafficType(
            client,
            response['id'],
            response['name'],
            response['displayAttributeId']
        )
