from __future__ import absolute_import, division, print_function, \
    unicode_literals
from identify.resources.base_resource import BaseResource


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
    }

    def __init__(self, data, client=None):
        '''
        '''
        BaseResource.__init__(self, data.get('id'), client)
        self._traffic_type_id = data.get('trafficTypeId')
        self._display_name = data.get('displayName')
        self._description = data.get('description')
        self._data_type = data.get('dataType')
        self._is_searchable = data.get('isSearchable')

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

    def delete(self, identify_client=None):
        '''
        Delete this attribute

        :param identify_client: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call
        '''
        if identify_client is not None:
            amc = identify_client.attribute
        elif self._client is not None:
            from identify.microclients import AttributeMicroClient
            amc = AttributeMicroClient(self._client)
        else:
            raise ClientRequiredError('An IdentityMicroClient is required')

        return amc.delete(self)
