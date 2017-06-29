from identify.resources import Identity
from identify.util.exceptions import HTTPResponseError, \
    UnknownIdentifyClientError
from identify.util.logger import LOGGER


class IdentityMicroClient:
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

    def __init__(self, http_client):
        '''
        '''
        self._http_client = http_client

    def save(self, identity):
        '''
        '''
        try:
            data = identity.to_dict() if isinstance(identity, Identity) else identity
            response = self._http_client.make_request(
                self._endpoint['create'],
                data,
                key=data.get('key'),
                trafficTypeId=data.get('trafficTypeId'),
                environmentId=data.get('environmentId'),
            )
        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Identity not created.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

        return Identity(response, self._http_client)

    def save_all(self, identities):
        '''
        entities: { key: { attr_id: value, ...} }
        '''
        # TODO: Validate!
        try:
            # convert Identity objects to dict if necessary
            to_save = [
                i.to_dict() if isinstance(i, Identity) else i
                for i in identities
            ]
            response = self._http_client.make_request(
                self._endpoint['create_many'],
                to_save,
                trafficTypeId=to_save[0]['trafficTypeId'],
                environmentId=to_save[0]['environmentId']
            )

            successful = [
                Identity(i, self._http_client)
                for i in response['objects']
            ]

            failed = [
                {
                    'object': Identity(i['object'], self._http_client),
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

    def update(self, identity):
        '''
        '''
        try:
            data = identity.to_dict() if isinstance(identity, Identity) else identity
            response = self._http_client.make_request(
                self._endpoint['update'],
                data,
                key=data.get('key'),
                trafficTypeId=data.get('trafficTypeId'),
                environmentId=data.get('environmentId'),
            )
        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Identity not created.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

        return Identity(response, self._http_client)

    def patch(self, identity):
        '''
        '''
        try:
            data = identity.to_dict() if isinstance(identity, Identity) else identity
            response = self._http_client.make_request(
                self._endpoint['patch'],
                data,
                key=data.get('key'),
                trafficTypeId=data.get('trafficTypeId'),
                environmentId=data.get('environmentId'),
            )
        except HTTPResponseError as e:
            LOGGER.error('Call to Identify API failed. Identity not created.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError()

        return Identity(response, self._http_client)

    def delete_all_attributes(self, identity):
        '''
        '''
        return self.delete_all_attributes_by_id(
            identity.traffic_type_id,
            identity.environment_id,
            identity.key
        )

    def delete_all_attributes_by_id(self, traffic_type_id, environment_id, key):
        '''
        '''
        try:
            self._http_client.make_request(
                self._endpoint['delete_attributes'],
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
