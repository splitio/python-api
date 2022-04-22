from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class Workspace(BaseResource):
    '''
    '''
    _schema = {
        'id': 'string',
        'name': 'string',
        'requiresTitleAndComments': 'boolean'
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('id'), client)
        self._id = data.get('id')
        self._name = data.get('name')
        self._requiresTitleAndComments = data.get('requiresTitleAndComments')

    @property
    def name(self):
        return self._name

    def add_environment(self, data, apiclient=None):
        '''
        Add a new environment associated with this workspace.

        :param apiclient: If this instance wasn't returned by the client,
            the environmentClient instance should be passed in order to perform the
            http call
        '''
        imc = require_client('Environment', self._client, apiclient)
        environment = as_dict(data)
        workspaceId = self._id
        return imc.add(environment, workspaceId)
        
    def delete_environment(self, environment_name, apiclient=None):
        '''
        delete environment associated with this workspace.

        :param apiclient: If this instance wasn't returned by the client,
            the environmentClient instance should be passed in order to perform the
            http call
        '''
        imc = require_client('Environment', self._client, apiclient)
        workspaceId = self._id
        return imc.delete(environment_name, workspaceId)

    def add_segment(self, data, traffic_type_name, apiclient=None):
        '''
        Add a new segment associated with this workspace.

        :param apiclient: If this instance wasn't returned by the client,
            the segmentClient instance should be passed in order to perform the
            http call
        '''
        imc = require_client('Segment', self._client, apiclient)
        segment = as_dict(data)
        workspaceId = self._id
        return imc.add(segment, traffic_type_name, workspaceId)
        
    def delete_segment(self, segment_name, apiclient=None):
        '''
        delete segment associated with this workspace.

        :param apiclient: If this instance wasn't returned by the client,
            the segmentClient instance should be passed in order to perform the
            http call
        '''
        imc = require_client('Segment', self._client, apiclient)
        workspaceId = self._id
        return imc.delete(segment_name, workspaceId)

    def add_split(self, data, traffic_type_name, apiclient=None):
        '''
        Add a new split associated with this workspace.

        :param apiclient: If this instance wasn't returned by the client,
            the splitClient instance should be passed in order to perform the
            http call
        '''
        imc = require_client('Split', self._client, apiclient)
        workspaceId = self._id
        return imc.add(data, traffic_type_name, workspaceId)
        
    def delete_split(self, split_name, apiclient=None):
        '''
        delete split associated with this workspace.

        :param apiclient: If this instance wasn't returned by the client,
            the splitClient instance should be passed in order to perform the
            http call
        '''
        imc = require_client('Split', self._client, apiclient)
        workspaceId = self._id
        return imc.delete(split_name, workspaceId)

    def get_rollout_statuses(self, apiclient=None):
        '''
        get list of rollout statuses

        :param apiclient: If this instance wasn't returned by the client,
            the splitClient instance should be passed in order to perform the
            http call
        '''
        imc = require_client('Workspace', self._client, apiclient)
        workspaceId = self._id
        return imc.get_rollout_statuses(workspaceId)

    def update(self, fieldName, fieldValue, apiclient=None):
        '''
        update workspace field

        :param fieldName: field name
        :param fieldValue: new field value
        '''
        imc = require_client('Workspace', self._client, apiclient)
        workspaceId = self._id
        return imc.update(workspaceId, fieldName, fieldValue)

    def delete(self, apiclient=None):
        '''
        delete current workspace instance
        '''
        imc = require_client('Workspace', self._client, apiclient)
        workspaceId = self._id
        return imc.delete(workspaceId)

