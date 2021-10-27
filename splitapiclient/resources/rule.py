from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.condition import Condition
from splitapiclient.resources.bucket import Bucket

class Rule():
    '''
    '''
    _schema = {
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
    }

    def __init__(self, data=None):
        '''
        '''
        if not data:
            data = {}
        self._condition = Condition(data.get('condition')).export_dict() if 'condition' in data else {}
        self._buckets = []
        if 'buckets' in data:
            for item in data.get('buckets'):
                self._buckets.append(Bucket(item).export_dict())
    
    def export_dict(self):
        return {'condition': self._condition, 'buckets': self._buckets}
