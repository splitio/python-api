from __future__ import absolute_import, division, print_function, \
    unicode_literals
from identify.resources.base_resource import BaseResource
from identify.util.exceptions import HTTPResponseError, MethodNotApplicable, \
    UnknownIdentifyClientError
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
            'method': 'POST',
            'url_template': ('trafficTypes/{trafficTypeId}/environments'
                             '/{environmentId}/identities'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
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
            'response': False,
        },
    }

    _schema = {
        'key': 'string',
        'trafficTypeId': 'string',
        'environmentId': 'string',
        'values': 'object',
        'organizationId': 'string',
    }

    def __init__(self, client, key, traffic_type_id, environment_id,
                 values=None, organization_id=None):
        '''
        '''
        BaseResource.__init__(self, client, key)
        self._traffic_type_id = traffic_type_id
        self._key = key
        self._environment_id = environment_id
        self._values = values
        self._organization_id = organization_id

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

    def organization_id(self):
        return self._organization_id

    @classmethod
    def from_dict(cls, client, response):
        '''
        '''
        return Identity(
            client,
            response.get('key'),
            response.get('trafficTypeId'),
            response.get('environmentId'),
            response.get('values'),
            response.get('organizationId')
        )

    @classmethod
    def create(cls, client, key, traffic_type_id, environment_id, values,
               organization_id=None):
        '''
        '''
        try:
            response = client.make_request(
                cls._endpoint['create'],
                {
                    'key': key,
                    'trafficTypeId': traffic_type_id,
                    'environmentId': environment_id,
                    'values': values,
                    'organizationId': organization_id
                },
                key=key,
                trafficTypeId=traffic_type_id,
                environmentId=environment_id
            )
        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Identity not created.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

        return Identity.from_dict(client, response)

    @classmethod
    def create_many(cls, client, traffic_type_id, environment_id, identities,
                    organization_id=None):
        '''
        entities: { key: { attr_id: value, ...} }
        '''
        # TODO: Validate!
        try:
            response = client.make_request(
                cls._endpoint['create_many'],
                [
                    {
                        'key': key,
                        'trafficTypeId': traffic_type_id,
                        'environmentId': environment_id,
                        'values': identities[key],
                        'organizationId': organization_id,
                    }
                    for key in identities.keys()
                ],
                trafficTypeId=traffic_type_id,
                environmentId=environment_id
            )

            successful = [
                Identity.from_dict(client, i) for i in response['objects']
            ]

            failed = [
                {
                    'object': Identity.from_dict(client, i['object']),
                    'status': i['status'],
                    'message': i['message'],
                }
                for i in response['failed']
            ]

            return successful, failed

        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Identities not created.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

    @classmethod
    def update(cls, client, key, traffic_type_id, environment_id, values,
               organization_id=None):
        '''
        '''
        try:
            response = client.make_request(
                cls._endpoint['update'],
                {
                    'key': key,
                    'trafficTypeId': traffic_type_id,
                    'environmentId': environment_id,
                    'values': values,
                    'organizationId': organization_id,
                },
                key=key,
                trafficTypeId=traffic_type_id,
                environmentId=environment_id
            )
        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Identity not updated.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

        return Identity.from_dict(client, response)

    @classmethod
    def patch(cls, client, key, traffic_type_id, environment_id, values,
              organization_id=None):
        '''
        '''
        try:
            response = client.make_request(
                cls._endpoint['patch'],
                {
                    'key': key,
                    'trafficTypeId': traffic_type_id,
                    'environmentId': environment_id,
                    'values': values,
                    'organizationId': organization_id,
                },
                key=key,
                trafficTypeId=traffic_type_id,
                environmentId=environment_id
            )
        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Identity not patched.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

        return Identity.from_dict(client, response)

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
        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Identity not patched.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

    def update_this(self, values):
        '''
        '''
        return Identity.update(
            self._client, self.key, self.traffic_type_id,  self.environment_id,
            values, self._organization_id
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
            self._client, self.traffic_type_id, self.environment_id, self.key
        )
