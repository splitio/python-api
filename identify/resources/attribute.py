from __future__ import absolute_import, division, print_function, \
    unicode_literals
from identify.resources.base_resource import BaseResource
from identify.util.logger import LOGGER
from identify.util.exceptions import HTTPResponseError, \
    UnknownIdentifyClientError


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
        'dataType': 'string',
        'isSearchable': 'bool',
    }

    def __init__(self, client, id, traffic_type_id, display_name=None,
                 description=None, data_type=None, is_searchable=None):
        '''
        '''
        BaseResource.__init__(self, client, id)
        self._traffic_type_id = traffic_type_id
        self._display_name = display_name
        self._description = description
        self._data_type = data_type
        self._is_searchable = is_searchable

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

    @property
    def is_searchable(self):
        return self._is_searchable

    @classmethod
    def from_dict(cls, client, response):
        '''
        '''
        return Attribute(
            client,
            response.get('id'),
            response.get('trafficTypeId'),
            response.get('displayName'),
            response.get('description'),
            response.get('dataType'),
            response.get('isSearchable')
        )

    @classmethod
    def create(cls, client, id, traffic_type_id, display_name, description,
               data_type, is_searchable):
        '''
        '''
        # TODO: Validate!
        try:
            response = client.make_request(
                cls._endpoint['create'],
                {
                    'id': id,
                    'trafficTypeId': traffic_type_id,
                    'displayName': display_name,
                    'description': description,
                    'isSearchable': is_searchable,
                    'dataType': None if data_type is None else data_type.upper()
                },
                trafficTypeId=traffic_type_id
            )

            return Attribute.from_dict(client, response)

        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Attribute not created.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

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
        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Attribute not deleted.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

    def delete_this(self):
        '''
        '''
        return Attribute.delete(self._client, self._id, self.traffic_type_id)
