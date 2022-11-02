from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict
from splitapiclient.resources import Environment
from splitapiclient.resources import TrafficType
from splitapiclient.resources.default_rule import DefaultRule
from splitapiclient.resources.rule import Rule
from splitapiclient.resources.treatment import Treatment

class SplitDefinition(BaseResource):
    '''
    '''
    _schema = {
        'name': 'string',
        'environment': {
            'id': 'string',
            'name': 'string'
        },
        'trafficType' : {
            'id': 'string',
            'name': 'string'
        },
        'killed': 'boolean',
        'treatments': [{
            'name': 'string',
            'configurations': 'string',
            'description': 'string',
            'keys': [ 'string' ],
            'segments': [ 'string' ]
        }],
        'defaultTreatment': 'string',
        'baselineTreatment': 'string',      
        'trafficAllocation': 'number',
        'rules': [{
            'condition': {
                'combiner': 'string',
                'matchers': [{
                    'negate': 'boolean',
                    'type': { 'string' },
                    'attribute': 'string',
                    'string': 'string',
                    'bool' : 'boolean',
                    'strings' : [ 'string' ],
                    'number' : 'number',
                    'date' : 'number',
                    'between': { 'from': 'number', 'to' : 'umber' },
                    'depends': { 'splitName': 'string', 'treatment': 'string' }
                }]
            },
            'buckets': [{
                'treatment': 'string',
                'size': 'number'
            }]
        }],
        'defaultRule': [{
            'treatment': 'string',
            'size': 'number'
        }],
        'creationTime' : 'number',
        'lastUpdateTime' : 'number',
        'lastTrafficReceivedAt': 'number'
    }

    def __init__(self, data=None, environment_id=None, workspace_id=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('name'), client)
        self._name = data.get('name')
        self._environment = Environment(data.get('environment')) if 'environment' in data else {}
        self._trafficType = TrafficType(data.get('trafficType')) if 'trafficType' in data else {}
        self._treatments = []
        self._killed = data.get('killed') if 'killed' in data else False
        if 'treatments' in data:
            for item in data.get('treatments'):
                self._treatments.append(Treatment(item))
        self._default_treatment = data.get('defaultTreatment') if 'defaultTreatment' in data else ''
        self._baseline_treatment = data.get('baselineTreatment') if 'baselineTreatment' in data else ''
        self._traffic_allocation = data.get('trafficAllocation') if 'trafficAllocation' in data else 0
        self._rules = []
        for item in data.get('rules'):
            self._rules.append(Rule(item))
        self._default_rule = []
        for item in data.get('defaultRule'):
            self._default_rule.append(DefaultRule(item))
        self._workspace_id = workspace_id
        self._environment_id = environment_id
        self._lastUpdateTime = data.get('lastUpdateTime') if 'lastUpdateTime' in data else 0
        self._lastTrafficReceivedAt = data.get('lastTrafficReceivedAt') if 'lastTrafficReceivedAt' in data else 0
        self._creationTime = data.get('creationTime') if 'creationTime' in data else 0

    @property
    def name(self):
        return self._name
        
    def update_definition(self, data, apiclient=None):
        '''
        Update split definition in environment

        :param data: environment id
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: SplitDefinition instance
        :rtype: SplitDefinition
        '''
        imc = require_client('SplitDefinition', self._client, apiclient)
        return imc.update_definition(self._name, self._environment_id, self._workspace_id, data)

    def kill(self, apiclient=None):
        '''
        Kill split

        :param data: None
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: True if successful
        :rtype: Boolean
        '''
        imc = require_client('SplitDefinition', self._client, apiclient)
        return imc.kill(self._name, self._environment_id, self._workspace_id)

    def restore(self, apiclient=None):
        '''
        restore split

        :param data: None
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: True if successful
        :rtype: Boolean
        '''
        imc = require_client('SplitDefinition', self._client, apiclient)
        return imc.restore(self._name, self._environment_id, self._workspace_id)

    def submit_change_request(self, definition, operation_type, title, comment, approvers, rollout_status_id, apiclient=None):
        '''
        submit a change request for split definition

        :param data: ChangeRequest
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: ChangeRequest object
        :rtype: ChangeRequest
        '''
        data = {
            'split': {
                'name':self._name,
                'treatments': definition['treatments'],
                'defaultTreatment': definition['defaultTreatment'],
                'baselineTreatment': definition['baselineTreatment'],
                'rules': definition['rules'],
                'defaultRule': definition['defaultRule']
            },
            'operationType': operation_type,
            'title': title,
            'comment': comment,
            'approvers': approvers,
        }
        if rollout_status_id is not None:
            data['rolloutStatus'] = {'id': rollout_status_id}
        imc = require_client('ChangeRequest', self._client, apiclient)
        return imc.submit_change_request(self._environment_id, self._workspace_id, data)

