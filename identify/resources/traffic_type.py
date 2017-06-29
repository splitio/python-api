from __future__ import absolute_import, division, print_function, \
    unicode_literals
from identify.resources.base_resource import BaseResource
from identify.resources.attribute import Attribute
from identify.resources.identity import Identity
from identify.util.exceptions import ClientRequiredError


class TrafficType(BaseResource):
    '''
    '''
    _schema = {
        'id': 'string',
        'name': 'string',
        'displayAttributeId': 'string'
    }

    def __init__(self, data, client=None):
        '''
        '''
        BaseResource.__init__(self, data.get('id'), client)
        self._name = data.get('name')
        self._display_attribute_id = data.get('displayAttributeId')

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def display_attribute_id(self):
        return self._display_attribute_id

    def fetch_attributes(self, identify_client=None):
        '''
        '''
        if identify_client is not None:
            amc = identify_client.attribute
        elif self._client is not None:
            from identify.microclients import AttributeMicroClient
            amc = AttributeMicroClient(self._client)
        else:
            raise ClientRequiredError('An AttributeMicroClient is required')
        return amc.list(self.id)

    def add_attribute(self, data, identify_client=None):
        '''
        '''
        if identify_client is not None:
            amc = identify_client.attribute
        elif self._client is not None:
            from identify.microclients import AttributeMicroClient
            amc = AttributeMicroClient(self._client)
        else:
            raise ClientRequiredError('An AttributeMicroClient is required')

        attribute = data.to_dict() if isinstance(data, Attribute) else data
        if not attribute.get('trafficTypeId'):
            attribute['trafficTypeId'] = self.id
        return amc.create(attribute)

    def add_identity(self, data, identify_client=None):
        '''
        '''
        if identify_client is not None:
            imc = identify_client.identity
        elif self._client is not None:
            from identify.microclients import IdentityMicroClient
            imc = IdentityMicroClient(self._client)
        else:
            raise ClientRequiredError('An IdentityMicroClient is required')

        identity = data.to_dict() if isinstance(data, Identity) else data
        if not identity.get('trafficTypeId'):
            identity['trafficTypeId'] = self.id
        return imc.save(identity)

    def add_identities(self, data, identify_client=None):
        '''
        '''
        if identify_client is not None:
            imc = identify_client.identity
        elif self._client is not None:
            from identify.microclients.identity_microclient import IdentityMicroClient
            imc = IdentityMicroClient(self._client)
        else:
            raise ClientRequiredError('An IdentityMicroClient is required')

        identities = [
            i.to_dict() if isinstance(i, Identity) else i
            for i in data
        ]
        for item in identities:
            if not item.get('trafficTypeId'):
                item['trafficTypeId'] = self.id
        return imc.save_all(identities)

