from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict
from splitapiclient.resources import TrafficType

class Split(BaseResource):
    '''
    '''
    _schema = {
        'name': 'string',
        'description': 'string',
        'trafficType' : {
            'id': 'string',
            'namr': 'string'
        },
        'creationTime' : 'number',
        'id': 'string',
        'rolloutStatus': {
            'id': 'string',
            'name': 'string'
        },
        'rolloutStatusTimestamp': 'number',
        'tags': [{'name': 'string'}],
        'owners': [{'id':'string','type':'string'}]
    }

    def __init__(self, data=None, workspace_id=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('name'), client)
        self._name = data.get('name')
        self._description = data.get('description')
        self._trafficType = TrafficType(data.get('trafficType')) if 'trafficType' in data else {}
        self._workspace_id = workspace_id
        self._creationTime = data.get('creationTime') if 'creationTime' in data else 0
        self._tags = data.get('tags') if 'tags' in data else []
        self._id = data.get('id') if 'id' in data else None
        self._rolloutStatus = data.get('rolloutStatus') if 'rolloutStatus' in data else {}
        self._rolloutStatusTimestamp = data.get('rolloutStatusTimestamp') if 'rolloutStatusTimestamp' in data else 0
        self._owners = data.get('owners') if 'owners' in data else []

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description
        
    def update_description(self, new_description, apiclient=None):
        '''
        Update split description
        '''
        imc = require_client('Split', self._client, apiclient)
        return imc.update_description(self._name, new_description, self._workspace_id)

        
    def add_to_environment(self, environment_id, data, apiclient=None):
        '''
        Add split to environment

        :param data: environment id
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: SplitDefinition instance
        :rtype: SplitDefinition
        '''
        imc = require_client('Split', self._client, apiclient)
        return imc.add_to_environment(self._name, environment_id, self._workspace_id, data)

    def remove_from_environment(self, environment_id, comment="", title="", apiclient=None):
        '''
        Remove split from environment

        :param data: environment id
        :param data: title
        :param data: comment
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: SplitDefinition instance
        :rtype: SplitDefinition
        '''
        imc = require_client('Split', self._client, apiclient)
        return imc.remove_from_environment(self._name, environment_id, comment, title, self._workspace_id)

    def associate_tags(self, tags, apiclient=None):
        '''
        Add tags to split

        :param data: array of tags (strings)
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: True if successful
        :rtype: boolean
        '''
        imc = require_client('Split', self._client, apiclient)
        return imc.associate_tags(self._name, tags, self._workspace_id)
