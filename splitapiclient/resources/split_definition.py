from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict
from splitapiclient.resources import Environment
from splitapiclient.resources import TrafficType
from splitapiclient.resources.flag_set import FlagSet
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
                    'between': { 'from': 'number', 'to' : 'number' },
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
        'lastTrafficReceivedAt': 'number',
        'impressionsDisabled': 'boolean',
        'flagSets': [{
            'id': 'string',
            'type': 'string'
        }]
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
        self._impressionsDisabled = data.get('impressionsDisabled') if 'impressionsDisabled' in data else False        
        if 'treatments' in data:
            for item in data.get('treatments'):
                self._treatments.append(Treatment(item))
        self._default_treatment = data.get('defaultTreatment') if 'defaultTreatment' in data else ''
        self._baseline_treatment = data.get('baselineTreatment') if 'baselineTreatment' in data else ''
        self._traffic_allocation = data.get('trafficAllocation') if 'trafficAllocation' in data else 0
        self._rules = []
        for item in data.get('rules'):
            self._rules.append(Rule(item))
        self._flagSets = []
        if 'flagSets' in data:
            for item in data.get('flagSets'):
                self._flagSets.append(FlagSet(item))
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


    @property
    def environment(self):
        return None if self._environment.id == "" else self._environment
    
    @property
    def flag_sets(self):
        return None if len(self._flagSets) == 0 else self._flagSets 
    
    @property
    def traffic_type(self):
        return self._trafficType
    
    @property
    def killed(self):
        return self._killed
   
    @property
    def impressions_disabled(self):
        return self._impressionsDisabled
    
    @property
    def treatments(self):
        return None if len(self._treatments) == 0 else self._treatments 

    @property
    def default_treatment(self):
        return self._default_treatment
    
    @property
    def baseline_treatment(self):
        return self._baseline_treatment


    @property
    def traffic_allocation(self):
        return self._traffic_allocation
    
    @property
    def rules(self):
        return None if len(self._rules) == 0 else self._rules 
    
    @property
    def default_rule(self):
        return None if len(self._default_rule) == 0 else self._default_rule 
    
    @property
    def creation_time(self):
        return None if self._creationTime == 0 else self._creationTime

    @property
    def last_update_time(self):
        return None if self._lastUpdateTime == 0 else self._lastUpdateTime
    
    @property
    def last_traffic_received_at(self):
        return None if self._lastTrafficReceivedAt == 0 else self._lastTrafficReceivedAt

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

