from identify.resources.attribute import Attribute
from identify.util.exceptions import HTTPResponseError, \
    UnknownIdentifyClientError
from identify.util.logger import LOGGER


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
        '''
        try:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                trafficTypeId=traffic_type_id
            )
            return [Attribute(item) for item in response]
        except HTTPResponseError as e:
            LOGGER.error('Error retrieving items')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

    def create(self, attribute):
        '''
        '''
        # TODO: Validate!
        try:
            data = attribute.to_dict() if isinstance(attribute, Attribute) else attribute
            response = self._http_client.make_request(
                self._endpoint['create'],
                data,
                trafficTypeId=data['trafficTypeId']
            )

            return Attribute(response, self._http_client)

        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Attribute not created.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

    def delete(self, attribute):
        '''
        '''
        return self.delete_by_id(attribute.id, attribute.traffic_type_id)

    def delete_by_id(self, attribute_id, traffic_type_id):
        '''
        '''
        try:
            return self._http_client.make_request(
                self._endpoint['delete'],
                trafficTypeId=traffic_type_id,
                attributeId=attribute_id
            )
        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Attribute not deleted.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()
