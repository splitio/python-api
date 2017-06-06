from identify.resources.base_resource import BaseResource
from identify.util.logger import LOGGER
from identify.util.exceptions import HTTPResponseError


class Attribute(BaseResource):
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'trafficTypes/{trafficTypeId}/schema',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'create': {
            'method': 'PUT',
            'url_template': 'trafficTypes/{trafficTypeId}/schema',
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
            'url_template': 'trafficTypes/{trafficTypeId}/schema/{attributeId}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': False,
        },
    }

    _schema = {
        'id': 'string',
        'trafficTypeId': 'string',
        'displayName': 'string',
        'description': 'string',
        'dataType': 'string'
    }

    def __init__(self, client, id, traffic_type_id, display_name=None,
                 description=None, data_type=None):
        '''
        '''
        BaseResource.__init__(self, client, id)
        self._traffic_type_id = traffic_type_id
        self._display_name = display_name
        self._description = description
        self._data_type = data_type

    @property
    def id(self):
        return self._id

    @property
    def traffic_type_id(self):
        return self._traffic_type_id

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def data_type(self):
        return self._data_type

    @classmethod
    def _build_single_from_collection_response(cls, client, response):
        '''
        '''
        return Attribute(
            client,
            response['id'],
            response['trafficTypeId'],
            response['displayName'],
            response['description'],
            response['dataType']
        )

    def to_dict(self):
        temp = {
            'id': self.id,
            'trafficTypeId': self.traffic_type_id,
            'displayName': self.display_name,
            'description': self.description,
            'dataType': self.data_type
        }

        return temp

    @classmethod
    def create(cls, client, id, traffic_type_id, display_name, description,
               data_type):
        '''
        '''
        # TODO: Validate!
        try:
            client.make_request(
                cls._endpoint['create'],
                {
                    'id': id,
                    'trafficTypeId': traffic_type_id,
                    'displayName': display_name,
                    'description': description,
                    'dataType': data_type.upper()
                },
                trafficTypeId=traffic_type_id
            )
        except HTTPResponseError:
            LOGGER.error('Call to Identify API failed. Attribute not created. '
                         'returning empty result.')
            return None

    @classmethod
    def delete(cls, client, attribute_id, traffic_type_id):
        '''
        '''
        try:
            return client.make_request(
                cls._endpoint['delete'],
                trafficTypeId=traffic_type_id,
                attributeId=attribute_id
            )
        except HTTPResponseError:
            LOGGER.error('Call to Identify API failed. Attribute not deleted.')

    def delete_this(self):
        '''
        '''
        return Attribute.delete(self._client, self._id, self.traffic_type_id)
