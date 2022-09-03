from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import as_dict, require_client
from splitapiclient.resources.attribute import Attribute

class TrafficType(BaseResource):
    '''
    '''
    _schema = {
        'id': 'string',
        'name': 'string',
        'displayAttributeId': 'string',
    }

    def __init__(self, data=None, workspaceId=None, client=None):
        '''
        Constructor
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('id'), client)
        self._id = data.get('id')
        self._name = data.get('name')
        self._display_attribute_id = data.get('displayAttributeId')
        self._workspace_id = workspaceId

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

    def fetch_attributes(self, apiclient=None):
        '''
        Fetch all attributes for this traffic type

        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: List of attributes associated with this traffic type
        :rtype: list(Attribute)
        '''
        amc = require_client('Attribute', self._client, apiclient)
        return amc.list(self.id, self._workspace_id)

    def add_attribute(self, data, apiclient=None):
        '''
        Add a new attribute associated with this traffic type

        :param data: Attribute instance or dict containing Attribute properties
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: Newly created attribute
        :rtype: Attribute
        '''
        amc = require_client('Attribute', self._client, apiclient)
        attribute = as_dict(data)
        attribute['trafficTypeId'] = self.id
        return amc.save(Attribute(attribute))

    def add_identity(self, data, apiclient=None):
        '''
        Add a new identity associated with this traffic type.

        :param data: Identity object or dict containing identity properties
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: newly created Identity
        :rtype: Identity
        '''
        imc = require_client('Identity', self._client, apiclient)
        identity = as_dict(data)
        identity['trafficTypeId'] = self.id
        return imc.save(identity)

    def import_attributes_from_json(self, json_data, apiclient=None):
        '''
        
        import attributes from JSON file into Split

        :param tt: workspace id,  json data, apiclient
        
        :returns: attribute
        
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: True if successful
        :rtype: boolean
        '''
        amc = require_client('Attribute', self._client, apiclient)
        return amc.import_attributes_from_json(self._workspace_id, self.id, data=json_data)


    def add_identities(self, data, apiclient=None):
        '''
        Add multiple new identities associated with this traffic type.

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
            item['trafficTypeId'] = self.id
        return imc.save_all(identities)
