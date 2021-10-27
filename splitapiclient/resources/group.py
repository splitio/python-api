from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class Group(BaseResource):
    '''
    '''
    _schema = {
        'id': 'string',
        'type': 'string',
        'name': 'string',
        'description': 'string'
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('id'), client)
        self._id = data.get('id')
        self._type = 'group'
        self._name = data.get('name')
        self._description = data.get('description') if 'description' in data else ''

    @property
    def name(self):
        return self._name

