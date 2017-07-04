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
        Constructor
        '''
        BaseResource.__init__(self, data.get('id'), client)
        self._name = data.get('name')
        self._display_attribute_id = data.get('displayAttributeId')

    @property
    def name(self):
        return self._name

    @property
    def display_attribute_id(self):
        return self._display_attribute_id

    @name.setter
    def name(self, new):
        self._name = new

    @display_attribute_id.setter
    def display_attribute_id(self, new):
        self._display_attribute_id = new

    def fetch_attributes(self, identify_client=None):
        '''
        Fetch all attributes for this traffic type

        :param identify_client: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: List of attributes associated with this traffic type
        :rtype: list(Attribute)
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
        Add a new attribute associated with this traffic type

        :param data: Attribute instance or dict containing Attribute properties
        :param identify_client: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: Newly created attribute
        :rtype: Attribute
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
        Add a new identity associated with this traffic type.

        :param data: Identity object or dict containing identity properties
        :param identify_client: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: newly created Identity
        :rtype: Identity
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
        Add multiple new identities associated with this traffic type.

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

