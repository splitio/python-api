from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict
from splitapiclient.resources import TrafficType
import csv

class LargeSegmentDefinition(BaseResource):
    '''
    '''
    _schema = {
        'id': 'string',
        'name': 'string',
        'environment': {
            'id': 'string',
            'name':'string'
        },
        'trafficType' : {
            'id': 'string',
            'name': 'string'
        },
        'creationTime' : 'number',
        'workspaceId': 'string'  
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('name'), client)
        self._id = data.get('id')
        self._name = data.get('name')
        self._environment = data.get('environment')
        self._trafficType = TrafficType(data.get('trafficType')) if 'trafficType' in data else {}
        self._creationTime = data.get('creationTime') if 'creationTime' in data else 0
        self._workspaceId = data.get('workspaceId')

    @property
    def name(self):
        return self._name

    @property
    def traffic_type(self):
        return None if self._trafficType == {} else self._trafficType
        
    @property
    def environment(self):
        return self._environment

    @property
    def creation_time(self):
        return None if  self._creationTime==0 else self._creationTime

    @property
    def id(self):
        return self._id

    @property
    def workspaceId(self):
        return self._workspaceId

    def remove_all_members(self, title, comment, approvers, apiclient=None):
        '''
        remove all members from the large segment
        '''

        workspaceId = self._workspaceId 
        imc = require_client('LargeSegmentDefinition', self._client, apiclient)
        return imc.remove_all_members(workspaceId, self._environment['id'], self._name,  title, comment, approvers)

    def submit_upload(self, title, comment, approvers,   filePath, apiclient=None):
        '''
        submit a change request for large segment definition

        :param title: title of the change request
        :param comment: comment of the change request
        :param approvers: list of approvers - if approvals are required
        :param workspace_id: workspace id
        :param filePath: path to the file to be uploaded
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: ChangeRequest object
        '''
        workspaceId = self._workspaceId
        imc = require_client('LargeSegmentDefinition', self._client, apiclient)
        result =  imc.submit_upload(workspaceId, self._environment['id'], self._name, title,comment, approvers)
        if result:
            uploadResult =  imc.upload_file(result, filePath)
        return uploadResult if uploadResult else result