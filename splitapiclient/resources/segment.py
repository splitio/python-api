from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict
from splitapiclient.resources import TrafficType

class Segment(BaseResource):
    '''
    '''
    _schema = {
        'name': 'string',
        'description': 'string',
        'trafficType' : {
            'id': 'string',
            'name': 'string'
        },
        'workspaceId' : 'string',
        'creationTime' : 'number',
        'tags': [{'name': 'string'}]
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('name'), client)
        self._name = data.get('name')
        self._description = data.get('description')
        self._trafficType = TrafficType(data.get('trafficType')) if 'trafficType' in data else {}
        self._workspace_id = data.get('workspaceId')
        self._tags = data.get('tags') if 'tags' in data else []
        self._creationTime = data.get('creationTime') if 'creationTime' in data else 0

            
    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description
        
    def add_to_environment(self, environment_id, apiclient=None):
        '''
        Add segment to environment

        :param data: environment id
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: SegmentDefinition instance
        :rtype: SegmentDefinition
        '''
        imc = require_client('Segment', self._client, apiclient)
        return imc.add_to_environment(self._name, environment_id)

    def remove_from_environment(self, environment_id, apiclient=None):
        '''
        Remove segment from environment

        :param data: environment id
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: True if successful
        :rtype: Boolean
        '''
        imc = require_client('Segment', self._client, apiclient)
        return imc.remove_from_environment(self._name, environment_id)

