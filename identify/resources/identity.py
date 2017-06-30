from __future__ import absolute_import, division, print_function, \
    unicode_literals
from identify.resources.base_resource import BaseResource


class Identity(BaseResource):
    '''
    '''
    _schema = {
        'key': 'string',
        'trafficTypeId': 'string',
        'environmentId': 'string',
        'values': 'object',
        'organizationId': 'string',
    }

    def __init__(self, data, client=None):
        '''
        '''
        BaseResource.__init__(self, None, client)
        self._traffic_type_id = data.get('trafficTypeId')
        self._key = data.get('key')
        self._environment_id = data.get('environmentId')
        self._values = data.get('values')
        self._organization_id = data.get('organizationId')

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

    @property
    def organization_id(self):
        return self._organization_id

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

    @organization_id.setter
    def organization_id(self, new):
        self._organization_id = new

    def save(self, identify_client=None):
        '''
        Save this Identity

        :param identify_client: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: newly saved Identity object
        :rtype: Identity
        '''
        if identify_client is not None:
            imc = identify_client.identity
        elif self._client is not None:
            from identify.microclients import IdentityMicroClient
            imc = IdentityMicroClient(self._client)
        else:
            raise ClientRequiredError('An IdentityMicroClient is required')

        return imc.save(self.to_dict())

    def update(self, identify_client=None):
        '''
        Update this Identity

        :param identify_client: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: newly saved Identity object
        :rtype: Identity
        '''
        if identify_client is not None:
            imc = identify_client.identity
        elif self._client is not None:
            from identify.microclients import IdentityMicroClient
            imc = IdentityMicroClient(self._client)
        else:
            raise ClientRequiredError('An IdentityMicroClient is required')

        return imc.update(self.to_dict())

    def delete_attributes(self, identify_client=None):
        '''
        Delete all attributes from this Identity

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
            raise ClientRequiredError('An IdentityMicroClient is required')

        return imc.delete_all_attributes(self)
