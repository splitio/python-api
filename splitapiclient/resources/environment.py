from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class Environment(BaseResource):
    '''
    '''
    _schema = {
        'id': 'string',
        'name': 'string',
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('id'), client)
        self._name = data.get('name')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new):
        self._name = new

    def add_identity(self, data, apiclient=None):
        '''
        Add a new identity associated with this environment.

        :param data: Identity object or dict containing identity properties
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call
        '''
        imc = require_client('Identity', self._client, apiclient)
        identity = as_dict(data)
        identity['environmentId'] = self.id
        return imc.save(identity)

    def add_identities(self, data, apiclient=None):
        '''
        Add multiple new identities associated with this environment.

        :param data: list ofIdentity objects or dicts containing identity
            properties
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: tuple with successful and failed items. Succesful items
            are Identity objects. Failed ones will contain the Identity object
            for the failed item togegther with a status code and a message
        :rtype: tuple
        '''
        imc = require_client('Identity', self._client, apiclient)
        identities = [as_dict(i) for i in data]
        for item in identities:
            item['environmentId'] = self.id
        return imc.save_all(identities)
