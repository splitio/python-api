from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class FlagSet(BaseResource):
    '''
    '''
    _schema = {
        "id" : "string",
        "name": "string",
        "description": "string",
        "workspace": {
            "id": "string",
            "type": "string"
        },
        "createdAt": "string",
        "type": "string"
    }

    def __init__(self, data=None, workspace_id=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('id'), client)
        self._id = data.get('id')
        self._name = data.get('name')
        self._description = data.get('desription')
        self._workspace_id = workspace_id or (data.get('workspace') and data.get('workspace').get('id'))
        self._createdAt = data.get('createdAt')
        self._client = client

    @property
    def description(self):
        return self._description

    @property
    def workspace_id(self):
        return self._workspace_id
    
    @property
    def createdAt(self):
        return self._createdAt
            
    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id


    def list(self,  workspaceId=None, apiclient=None):
        '''
        list flag sets in a workspace
        '''
        imc = require_client('FlagSet', self._client, apiclient)
        workspaceId = self._workspace_id or workspaceId
        return imc.list(workspaceId)


    def find(self, flagSetName, workspaceId=None, apiclient=None):
        '''
        get a flag set by id
        '''
        imc = require_client('FlagSet', self._client, apiclient)

        return imc.find(flagSetName, workspaceId)



    def get(self, flagSetId, apiclient=None):
        '''
        get a flag set by id
        '''
        imc = require_client('FlagSet', self._client, apiclient)
        flag_set_id = self._id or flagSetId

        return imc.get(flag_set_id)



    def add(self, apiclient=None):
        '''
        add a flag set
        '''
        imc = require_client('FlagSet', self._client, apiclient)
        flagsetId = self._id
        workspaceId = self._workspace_id
        return imc.add(flagsetId, workspaceId)
    
    def delete(self, flagSetId=None, apiclient=None):
        '''
        delete current flagSet instance
        '''
        imc = require_client('FlagSet', self._client, apiclient)
        flagsetId =  flagSetId or self._id
        return imc.delete(flagsetId)
