from identify.resources.base_resource import BaseResource
from identify.util.exceptions import HTTPResponseError, MethodNotApplicable
from identify.util.logger import LOGGER


class Identity(BaseResource):
    '''
    '''
    _endpoint = {
        'create': {
            'method': 'PUT',
            'url_template': ('trafficTypes/{trafficTypeId}/environments'
                             '/{environmentId}/identities/{key}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'create_many': {
            'method': 'PUT',
            'url_template': ('trafficTypes/{trafficTypeId}/environments'
                             '/{environmentId}/identities'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': False,
        },
        'update': {
            'method': 'POST',
            'url_template': ('trafficTypes/{trafficTypeId}/environments'
                             '/{environmentId}/identities/{key}/patch'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'patch': {
            'method': 'PATCH',
            'url_template': ('trafficTypes/{trafficTypeId}/environments'
                             '/{environmentId}/identities/{key}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'delete_attributes': {
            'method': 'DELETE',
            'url_template': ('trafficTypes/{trafficTypeId}/environments'
                             '/{environmentId}/identities/{key}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
    }

    _schema = {
        'key': 'string',
        'trafficTypeId': 'string',
        'environmentId': 'string',
        'values': 'object',
    }

    def __init__(self, client, key, traffic_type_id, environment_id,
                 values=None):
        '''
        '''
        BaseResource.__init__(self, client, id)
        self._traffic_type_id = traffic_type_id
        self._key = key
        self._environment_id = environment_id
        self._values = values

    @property
    def key(self):
        return self._id

    @property
    def traffic_type_id(self):
        return self._traffic_type_id

    @property
    def environment_id(self):
        return self._environment_id

    @property
    def values(self):
        return self._values

    @classmethod
    def _build_single_from_collection_response(cls, client, response):
        '''
        '''
        raise MethodNotApplicable()

    @classmethod
    def create(cls, client, key, traffic_type_id, environment_id, values):
        '''
        '''
        try:
            response = client.make_request(
                cls._endpoint['create'],
                {
                    'key': key,
                    'trafficTypeId': traffic_type_id,
                    'environmentId': environment_id,
                    'values': values
                },
                key=key,
                trafficTypeId=traffic_type_id,
                environmentId=environment_id
            )
        except HTTPResponseError:
            LOGGER.error('Call to Identify API failed. Identity not created. '
                         'returning empty result.')
            return None

        return Identity(
            client,
            response['key'],
            response['trafficTypeId'],
            response['environmentId'],
            response['values']
        )

    @classmethod
    def create_many(cls, client, traffic_type_id, environment_id, entities):
        '''
        entities: { key: { attr_id: value, ...} }
        '''
        # TODO: Validate!
        try:
            client.make_request(
                cls._endpoint['create_many'],
                [
                    {
                        'key': key,
                        'trafficTypeId': traffic_type_id,
                        'environmentId': environment_id,
                        'values': entities[key]
                    }
                    for key in entities.keys()
                ],
                trafficTypeId=traffic_type_id,
                environmentId=environment_id
            )
        except HTTPResponseError:
            LOGGER.error('Call to Identify API failed. Identities not created.')

    @classmethod
    def update(cls, client, key, traffic_type_id, environment_id, values):
        '''
        '''
        try:
            response = client.make_request(
                cls._endpoint['update'],
                {
                    'key': key,
                    'trafficTypeId': traffic_type_id,
                    'environmentId': environment_id,
                    'values': values
                },
                key=key,
                trafficTypeId=traffic_type_id,
                environmentId=environment_id
            )
        except HTTPResponseError:
            LOGGER.error('Call to Identify API failed. Identity not updated. '
                         'Returning empty result')
            return None

        return Identity(
            client,
            response['key'],
            response['trafficTypeId'],
            response['environmentId'],
            response['values']
        )

    @classmethod
    def patch(cls, client, key, traffic_type_id, environment_id, values):
        '''
        '''
        try:
            response = client.make_request(
                cls._endpoint['patch'],
                {
                    'key': key,
                    'trafficTypeId': traffic_type_id,
                    'environmentId': environment_id,
                    'values': values
                },
                key=key,
                trafficTypeId=traffic_type_id,
                environmentId=environment_id
            )
        except HTTPResponseError:
            LOGGER.error('Call to Identify API failed. Identity not patched. '
                         'Returning empty result')
            return None

        return Identity(
            client,
            response['key'],
            response['trafficTypeId'],
            response['environmentId'],
            response['values']
        )

    @classmethod
    def delete_all_attributes(cls, client, traffic_type_id, environment_id,
                              key):
        '''
        '''
        try:
            client.make_request(
                cls._endpoint['delete_attributes'],
                key=key,
                trafficTypeId=traffic_type_id,
                environmentId=environment_id
            )
        except HTTPResponseError:
            LOGGER.error('Call to Identify API failed. Identity not patched.')

    def update_this(self, values):
        '''
        '''
        return Identity.update(
            self._client, self.key, self.traffic_type_id,  self.environment_id,
            values
        )

    def patch_this(self, values):
        '''
        '''
        return Identity.patch(
            self._client, self.key, self.traffic_type_id,  self.environment_id,
            values
        )

    def delete_attributes_this(self):
        '''
        '''
        return Identity.delete_all_attributes(
            self.client, self.key, self.traffic_type_id, self.environment_id
        )
