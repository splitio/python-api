from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class APIKey(BaseResource):
    '''
    '''
    _schema = {
        'key': 'string',
        'name': 'string',
        'apiKeyType': 'string',
        'organization': {
            'id': 'string',
            'type': 'string'
        },
        'createdBy': {
            'type': 'string',
            'id': 'string',
            'name': 'string'
        },
        'createdAt': 'number',
        'environments': [
        {
            'type': 'string',
            'id': 'string'
        }],
        'workspace': {
            'type': 'string',
            'id': 'string'
        },
        type: 'api_key'
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('key'), client)
        self._key = data.get('key')
        self._name = data.get('name')
        self._apiKeyType = data.get('apiKeyType')
        self._createdBy = data.get('createdBy')
        self._created_at = data.get('createdAt')
        self._environments = data.get('environments') if 'environments' in data else []
        self._workspace = data.get('workspace') if 'workspace' in data else {}
        self._type = data.get('type')

    @property
    def key(self):
        return self._key

