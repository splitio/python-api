from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict

class User(BaseResource):
    '''
    '''
    _schema = {
        'id': 'string',
        'type': 'string',
        'name': 'string',
        'email': 'string',
        'status': 'string',
        'groups': [
        {
            'type': 'string',
            'id': 'string'
        }]
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('id'), client)
        self._id = data.get('id')
        self._type = 'user'
        self._name = data.get('name')
        self._email = data.get('email')
        self._status = data.get('status')
        self._groups = data.get('groups') if 'groups' in data else ''
            
    @property
    def email(self):
        return self._email

    def update_user(self, data, apiclient=None):
        '''
        Update user info
        '''
        imc = require_client('User', self._client, apiclient)
        return imc.update_user(self._id, data)

    def update_user_group(self, data, apiclient=None):
        '''
        Update user group
        '''
        imc = require_client('User', self._client, apiclient)
        return imc.update_user_group(self._id, data)

