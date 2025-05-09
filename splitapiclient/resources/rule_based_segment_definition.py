from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict
from splitapiclient.resources import TrafficType
from splitapiclient.resources import Environment
import csv

class RuleBasedSegmentDefinition(BaseResource):
    '''
    Resource class for rule-based segment definitions
    '''
    _schema = {
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
        'excludedKeys' : [ 'string' ],
        'excludedSegments' : [{
            'name': 'string',
            'type': 'string'
        }],
        'rules' : [{
            'condition': {
                'combiner': 'string',
                'matchers': [{
                    'type': 'string',
                    'attribute': 'string',
                    'string': 'string',
                    'bool' : 'boolean',
                    'strings' : [ 'string' ],
                    'number' : 'number',
                    'date' : 'number',
                    'between': { 'from': 'number', 'to' : 'umber' },
                    'depends': { 'splitName': 'string', 'treatment': 'string' }
                }]
            }
        }]
    }

    def __init__(self, data=None, client=None):
        '''
        Constructor for RuleBasedSegmentDefinition
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('name'), client)
        self._name = data.get('name')
        self._environment = data.get('environment')
        self._trafficType = TrafficType(data.get('trafficType')) if 'trafficType' in data else {}
        self._creationTime = data.get('creationTime') if 'creationTime' in data else 0
            
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
    def tags(self):
        return self._tags

    @property
    def creation_time(self):
        return None if self._creationTime==0 else self._creationTime

    def update(self, data):
        '''
        Update RuleBasedSegmentDefinition object.

        :param data: dictionary of data to update

        :returns: RuleBasedSegmentDefinition object
        :rtype: RuleBasedSegmentDefinition
        '''
        imc = require_client('RuleBasedSegmentDefinition', self._client)
        return imc.update(self._name, self._environment['id'], self._client._workspace_id, data)

    def submit_change_request(self, rules, operation_type, title, comment, approvers, rollout_status_id, workspace_id, apiclient=None):
        '''
        submit a change request for rule-based segment definition

        :param rules: dictionary of rules to update
        :param operation_type: operation type
        :param title: title of the change request
        :param comment: comment for the change request
        :param approvers: list of approvers
        :param rollout_status_id: rollout status id
        :param workspace_id: id of the workspace
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: ChangeRequest object
        :rtype: ChangeRequest
        '''
        data = {
            'ruleBasedSegment': {
                'name':self._name,
                'rules': rules,
            },
            'operationType': operation_type,
            'title': title,
            'comment': comment,
            'approvers': approvers,
        }
        if rollout_status_id is not None:
            data['rolloutStatus'] = {'id': rollout_status_id}
        imc = require_client('ChangeRequest', self._client, apiclient)
        return imc.submit_change_request(self._environment['id'], workspace_id, data)
