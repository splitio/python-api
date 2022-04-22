from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict

class Restriction(BaseResource):
    '''
    '''
    _schema = {
        "operations" : {
            "view" : True
        },
        "resourcePermissions" : {
            "view" : [{
                "name" : "name",
                "id" : "id",
                "type" : "user"
            }]
        },
        "resource" : {
            "name" : "name",
            "id" : "id",
            "type" : "workspace"
        },
        "id" : "id",
        "type" : "restriction"
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('id'), client)
        self._id = data.get('id')
        self._type = data.get('type')
        self._resourcePermissions = data.get('resourcePermissions') if 'resourcePermissions' in data else {}
        self._resource = data.get('resource') if 'resource' in data else {}
                
    def update(self, fieldName, fieldValue, apiclient=None):
        '''
        update restirction field

        :param fieldName: field name
        :param fieldValue: new field value
        '''
        imc = require_client('Restriction', self._client, apiclient)
        RestrictioneId = self._id
        return imc.update(RestrictioneId, fieldName, fieldValue)
