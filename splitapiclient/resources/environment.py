from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class Environment(BaseResource):
    '''
    '''
    _schema = {
        "creationTime" : 0,
        "production": False,
        "dataExportPermissions" : {
            "areExportersRestricted" : False,
            "exporters" : [{
              "name" : "string",
              "id" : "string",
              "type" : "string"
            }]
        },
        "environmentType" : "string",
        "workspaceIds" : [ "string" ],
        "name" : "string",
        "changePermissions" : {
            "areApproversRestricted" : False,
            "allowKills" : False,
            "areEditorsRestricted" : False,
            "areApprovalsRequired" : False,
            "approvers" : [ {
              "name" : "string",
              "id" : "string",
              "type" : "string"
            }],
            "editors" : [ {
              "name" : "string",
              "id" : "string",
              "type" : "string"
            }]
        },
        "type": "environment",
        "id" : "string",
        "orgId" : "string",
        "status" : "string"
    }

    def __init__(self, data=None, workspace_id=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('id'), client)
        self._id = data.get('id')
        self._name = data.get('name')
        self._production = data.get('production')
        self._workspace_id = workspace_id
        self._creationTime = data.get('creationTime')
        self._dataExportPermissions = data.get('dataExportPermissions')
        self._status = data.get('status')
        self._type = data.get('type')
        self._orgId = data.get('orgId')
        self._changePermissions = data.get("changePermissions") if "changePermissions" in data else {}
        self._client = client

    @property
    def workspace_id(self):
        return self._workspace_id
            
    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def production(self):
        return self._production

    def update_name(self, new_name, apiclient=None):
        '''
        Update environment name
        '''
        imc = require_client('Environment', self._client, apiclient)
        environment = as_dict({'name':self._name, 'production':self._production, 'id':self._id})
        workspaceId = self._workspace_id
        return imc.update_name(new_name, environment, workspaceId)

    def add_identity(self, data, apiclient=None):
        '''
        Add a new identity associated with this environment.

        :param data: Identity object or dict containing identity properties
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call
        '''
        imc = require_client('Identity', self._client, apiclient)
        identity = as_dict(data)
        identity['environmentId'] = self.id
        return imc.save(identity)

    def add_identities(self, data, apiclient=None):
        '''
        Add multiple new identities associated with this environment.

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
            item['environmentId'] = self.id
        return imc.save_all(identities)

    def update(self, fieldName, fieldValue, apiclient=None):
        '''
        update Environment field

        :param fieldName: field name
        :param fieldValue: new field value
        '''
        imc = require_client('Environment', self._client, apiclient)
        environmentId = self._id
        workspaceId = self._workspace_id
        return imc.update(environmentId, workspaceId, fieldName, fieldValue)

    def delete(self, apiclient=None):
        '''
        delete current environment instance
        '''
        imc = require_client('Environment', self._client, apiclient)
        environmentId = self._id
        workspaceId = self._workspace_id
        return imc.delete(environmentId, workspaceId)
