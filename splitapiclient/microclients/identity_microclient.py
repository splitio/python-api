from splitapiclient.resources import Identity
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER


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
        Constructor
        '''
        self._http_client = http_client

    def save(self, identity):
        '''
        Save an identity

        :param identity: Identity instance or dict containing keys with identity
            properties

        :returns: newly created Identity
        :rtype: Identity
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
            LOGGER.error('Call to Split API failed. Identity not created.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownApiClientError()

        return Identity(response, self._http_client)

    def save_all(self, identities):
        '''
        Save multiple identities at once

        :param identities: array of Identity instances or dicts containing keys
            with identity's properties

        :returns: tuple with successful and failed items. Succesful items
            are Identity objects. Failed ones will contain the Identity object
            for the failed item togegther with a status code and a message
        :rtype: tuple
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
            LOGGER.error('Call to Split API failed. Identities not created.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownApiClientError()

    def update(self, identity):
        '''
        Update an existing identity

        :param identity: Identity instance or dict containing keys with identity
            properties

        :returns: updated Identity
        :rtype: Identity
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
            LOGGER.error('Call to Split API failed. Identity not created.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownApiClientError()

        return Identity(response, self._http_client)

    def patch(self, identity):
        '''
        Patch an existing identity

        :param identity: Identity instance or dict containing keys with identity
            properties

        :returns: patched Identity
        :rtype: Identity
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
            LOGGER.error('Call to Split API failed. Identity not created.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownApiClientError()

        return Identity(response, self._http_client)

    def delete_by_instance(self, identity):
        '''
        Delete the identity

        :param identity: Identity instance
        '''
        return self.delete(
            identity.traffic_type_id,
            identity.environment_id,
            identity.key
        )

    def delete(self, traffic_type_id, environment_id, key):
        '''
        Delete the identity by specifying the traffic type id, the environment
        id and the identity's key instead of passing an Identity object.

        :param traffic_type_id: Identity's traffic type id
        :param environment_id: Identity's environment id
        :param key: Identity's key
        '''
        try:
            self._http_client.make_request(
                self._endpoint['delete_attributes'],
                key=key,
                trafficTypeId=traffic_type_id,
                environmentId=environment_id
            )
        except HTTPResponseError as e:
            LOGGER.error('Call to Split API failed. Identity not patched.')
            raise e
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownApiClientError()
