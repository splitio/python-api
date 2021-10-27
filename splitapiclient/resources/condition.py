from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.matcher import Matcher


class Condition():
    '''
    '''
    _schema = {
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
    }

    def __init__(self, data=None):
        '''
        '''
        if not data:
            data = {}
        self._combiner = data.get('combiner') if 'combiner' in data else ''
        self._matchers = []
        for item in data.get('matchers'):
            self._matchers.append(Matcher(item).export_dict())

    def export_dict(self):
        result = {'matchers':self._matchers}
        if self._combiner != "":
           result['combiner'] = self._combiner
        return result
