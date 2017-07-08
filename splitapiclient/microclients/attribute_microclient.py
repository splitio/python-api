from splitapiclient.resources import Attribute
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class AttributeMicroClient:
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

    def __init__(self, http_client):
        '''
        '''
        self._http_client = http_client

    def list(self, traffic_type_id):
        '''
        Returns a list of TrafficType objects.

        :param traffic_type_id: Id of the TrafficType whose attributes will be
            returned
        :rtype: list(TrafficType)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items'],
            trafficTypeId=traffic_type_id
        )
        return [Attribute(item, self._http_client) for item in response]

    def save(self, attribute):
        '''
        Create a new attribute.

        :param attribute: Attribute instance or dict with camelcase keys
            containing Attribute properties

        :returns: newly created attribute
        :rtype: Attribute
        '''
        data = as_dict(attribute)
        response = self._http_client.make_request(
            self._endpoint['create'],
            data,
            trafficTypeId=data.get('trafficTypeId')
        )
        return Attribute(response, self._http_client)

    def delete(self, attribute_id, traffic_type_id):
        '''
        Delete an attribute by specifying its id and it's traffic type id.

        :param attribute_id: attribute's id
        :param traffic_type_id: atribute's traffic type id
        '''
        return self._http_client.make_request(
            self._endpoint['delete'],
            trafficTypeId=traffic_type_id,
            attributeId=attribute_id
        )

    def delete_by_instance(self, attribute):
        '''
        Delete an attribute

        :param attribute: Attribute instance
        '''
        data = as_dict(attribute)
        return self.delete(
            data.get('id'),
            data.get('trafficTypeId')
        )
