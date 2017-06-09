from __future__ import absolute_import, division, print_function, \
    unicode_literals
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

    def __init__(self, client, id, name=None, display_attribute_id=None):
        '''
        '''
        BaseResource.__init__(self, client, id)
        self._name = name
        self._display_attribute_id = display_attribute_id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def display_attribute_id(self):
        return self._display_attribute_id

    def fetch_attributes(self):
        '''
        '''
        return Attribute.retrieve_all(self._client, trafficTypeId=self._id)

    def add_attribute(self, id, display_attribute_id, description, data_type):
        '''
        '''
        return Attribute.create(
            self._client,
            id,
            self._id,
            display_attribute_id,
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
