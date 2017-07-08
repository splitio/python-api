from splitapiclient.resources import Identity
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict
from splitapiclient.util.bulk_result import BulkOperationResult


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
        data = as_dict(identity)
        response = self._http_client.make_request(
            self._endpoint['create'],
            data,
            key=data.get('key'),
            trafficTypeId=data.get('trafficTypeId'),
            environmentId=data.get('environmentId'),
        )
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
        to_save = [as_dict(i) for i in identities]
        response = self._http_client.make_request(
            self._endpoint['create_many'],
            to_save,
            trafficTypeId=to_save[0].get('trafficTypeId'),
            environmentId=to_save[0].get('environmentId')
        )

        successful = [
            Identity(i, self._http_client)
            for i in response.get('objects', [])
        ]

        failed = [
            {
                'object': Identity(i['object'], self._http_client),
                'status': i['status'],
                'message': i['message'],
            }
            for i in response.get('failed', [])
        ]

        return BulkOperationResult(successful, failed, response.get('metadata'))

    def update(self, identity):
        '''
        Update an existing identity

        :param identity: Identity instance or dict containing keys with identity
            properties

        :returns: updated Identity
        :rtype: Identity
        '''
        data = as_dict(identity)
        response = self._http_client.make_request(
            self._endpoint['update'],
            data,
            key=data.get('key'),
            trafficTypeId=data.get('trafficTypeId'),
            environmentId=data.get('environmentId'),
        )
        return Identity(response, self._http_client)

    def patch(self, identity):
        '''
        Patch an existing identity

        :param identity: Identity instance or dict containing keys with identity
            properties

        :returns: patched Identity
        :rtype: Identity
        '''
        data = as_dict(identity)
        response = self._http_client.make_request(
            self._endpoint['patch'],
            data,
            key=data.get('key'),
            trafficTypeId=data.get('trafficTypeId'),
            environmentId=data.get('environmentId'),
        )
        return Identity(response, self._http_client)

    def delete(self, traffic_type_id, environment_id, key):
        '''
        Delete the identity by specifying the traffic type id, the environment
        id and the identity's key instead of passing an Identity object.

        :param traffic_type_id: Identity's traffic type id
        :param environment_id: Identity's environment id
        :param key: Identity's key
        '''
        self._http_client.make_request(
            self._endpoint['delete_attributes'],
            key=key,
            trafficTypeId=traffic_type_id,
            environmentId=environment_id
        )

    def delete_by_instance(self, identity):
        '''
        Delete the identity

        :param identity: Identity instance
        '''
        data = as_dict(identity)
        return self.delete(
            data.get('trafficTypeId'),
            data.get('environmentId'),
            data.get('key')
        )
