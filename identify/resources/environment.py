from __future__ import absolute_import, division, print_function, \
    unicode_literals
from identify.resources.base_resource import BaseResource
from identify.resources.identity import Identity


class Environment(BaseResource):
    '''
    '''
    _schema = {
        'id': 'string',
        'name': 'string',
    }

    def __init__(self, data, client=None):
        '''
        '''
        BaseResource.__init__(self, data.get('id'), client)
        self._name = data.get('name')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new):
        self._name = new

    def add_identity(self, data, identify_client=None):
        '''
        Add a new identity associated with this environment.

        :param data: Identity object or dict containing identity properties
        :param identify_client: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call
        '''
        if identify_client is not None:
            imc = identify_client.identity
        elif self._client is not None:
            from identify.microclients import IdentityMicroClient
            imc = IdentityMicroClient(self._client)
        else:
            raise ClientRequiredError('An IdentifyClient is required')

        identity = data.to_dict() if isinstance(data, Identity) else data
        if not identity.get('environmentId'):
            identity['environmentId'] = self.id
        return imc.save(identity)

    def add_identities(self, data, identify_client=None):
        '''
        Add multiple new identities associated with this environment.

        :param data: list ofIdentity objects or dicts containing identity
            properties
        :param identify_client: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: tuple with successful and failed items. Succesful items
            are Identity objects. Failed ones will contain the Identity object
            for the failed item togegther with a status code and a message
        :rtype: tuple
        '''
        if identify_client is not None:
            imc = identify_client.identity
        elif self._client is not None:
            from identify.microclients import IdentityMicroClient
            imc = IdentityMicroClient(self._client)
        else:
            raise ClientRequiredError('An IdentityMicroClient is required')

        # Convert identity objects to dicts if necessary before updating the
        # environmentId
        identities = [
            i.to_dict() if isinstance(i, Identity) else i
            for i in data
        ]
        for item in identities:
            if not item.get('environmentId'):
                item['environmentId'] = self.id
        return imc.save_all(identities)
