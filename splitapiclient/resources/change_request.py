from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict

class ChangeRequest(BaseResource):
    '''
    '''
    _schema = {
        'split': {
            'id': 'string',
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
            'openChangeRequestId' : 'number'
        },
        'segment': {
            'name': 'string',
            'keys': ['string']
        },
        'id': 'string',
        'status': 'string',
        'title': 'string',
        'comment': 'string',
        'approvers': ['string'],
        'operationType': 'string',
        'comments':[{
            'comment': 'string',
            'user': 'string',
            'role': 'string',
            'timestamp': 'number'
        }],
        'rolloutStatus': {
            'id': 'string',
            'type': 'string',
            'name': 'string'
        }
    }
    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('id'), client)
        self._id = data.get('id')
        self._status = data.get('status')
        self._title = data.get('title') if 'title' in data else ''
        self._comment = data.get('comment') if 'comment' in data else ''
        self._split = data.get('split') if 'split' in data else {}
        self._segment = data.get('segment') if 'segment' in data else {}
        self._operationType = data.get('operationType') if 'operationType' in data else ''
        self._environment = data.get('environment')
        self._approvers = []
        if 'approvers' in data:
            for item in data.get('approvers'):
                self._approvers.append(item)
        self._comments = []
        if 'comments' in data:
            for item in data.get('comments'):
                self._comments.append(item)
        self._rolloutStatus = data.get('rolloutStatus') if 'rolloutStatus' in data else {}
            
    @property
    def name(self):
        return self._name
        
    def update_status(self, new_status, comment, apiclient=None):
        '''
        Update change request status
        '''
        imc = require_client('ChangeRequest', self._client, apiclient)
        change_request_id = self._id
        return imc.update_status(change_request_id, new_status, comment)


        
