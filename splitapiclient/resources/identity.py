from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import as_dict, require_client


class Identity(BaseResource):
    '''
    '''
    _schema = {
        'key': 'string',
        'trafficTypeId': 'string',
        'environmentId': 'string',
        'values': 'object',
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, None, client)
        self._traffic_type_id = data.get('trafficTypeId')
        self._key = data.get('key')
        self._environment_id = data.get('environmentId')
        self._values = data.get('values')

    @property
    def key(self):
        return self._key

    @property
    def traffic_type_id(self):
        return self._traffic_type_id

    @property
    def environment_id(self):
        return self._environment_id

    @property
    def values(self):
        return self._values

    @key.setter
    def key(self, new):
        self._key = new

    @traffic_type_id.setter
    def traffic_type_id(self, new):
        self._traffic_type_id = new

    @environment_id.setter
    def environment_id(self, new):
        self._environment_id = new

    @values.setter
    def values(self, new):
        self._values = new

    def save(self, apiclient=None):
        '''
        Save this Identity

        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: newly saved Identity object
        :rtype: Identity
        '''
        imc = require_client('Identity', self._client, apiclient)
        return imc.save(self.to_dict())

    def update(self, apiclient=None):
        '''
        Update this Identity

        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: newly saved Identity object
        :rtype: Identity
        '''
        imc = require_client('Identity', self._client, apiclient)
        return imc.update(self.to_dict())

    def delete(self, apiclient=None):
        '''
        Delete all attributes from this Identity

        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call
        '''
        imc = require_client('Identity', self._client, apiclient)
        return imc.delete_by_instance(self)
