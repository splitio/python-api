from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client


class Attribute(BaseResource):
    '''
    '''
    _schema = {
        'id': 'string',
        'trafficTypeId': 'string',
        'displayName': 'string',
        'description': 'string',
        'dataType': 'string',
        'isSearchable': 'bool',
        'workspaceId' : 'string',
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('id'), client)
        self._id = data.get('id')
        self._traffic_type_id = data.get('trafficTypeId')
        self._display_name = data.get('displayName')
        self._description = data.get('description')
        self._data_type = data.get('dataType')
        self._is_searchable = data.get('isSearchable')
        self._workspace_id = data.get('workspaceId')

    @property
    def traffic_type_id(self):
        return self._traffic_type_id

    @property
    def display_name(self):
        return self._display_name

    @property
    def description(self):
        return self._description

    @property
    def data_type(self):
        return self._data_type

    @property
    def is_searchable(self):
        return self._is_searchable

    @traffic_type_id.setter
    def traffic_type_id(self, new):
        self._traffic_type_id = new

    @display_name.setter
    def display_name(self, new):
        self._display_name = new

    @description.setter
    def description(self, new):
        self._description = new

    @data_type.setter
    def data_type(self, new):
        self._data_type = new

    @is_searchable.setter
    def is_searchable(self, new):
        self._is_searchable = new

    def save(self, apiclient=None):
        '''
        Save this attribute

        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call
        '''
        amc = require_client('Attribute', self._client, apiclient)
        return amc.save(self)

    def delete(self, apiclient=None):
        '''
        Delete this attribute

        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call
        '''
        amc = require_client('Attribute', self._client, apiclient)
        return amc.delete_by_instance(self)
