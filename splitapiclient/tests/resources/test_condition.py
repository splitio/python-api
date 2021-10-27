from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources.condition import Condition

class TestCondition:
    '''
    Tests for the Condition and Matcher classes
    '''
    def test_constructor(self):
        '''
        '''
        data = {
            'combiner': 'AND',
            'matchers': [{
                'negate': True,
                'type': 'IN_STRING',
                'attribute': 'country',
                'string': 'US',
                'bool' : False,
                'strings' : [ 'US', 'Canada' ],
                'number' : 10,
                'date' : 1234567,
                'between': { 'from': 10, 'to' : 20 },
                'depends': { 'splitName': 'split1', 'treatment': 'tr1' }
            }]
        }
        cd = Condition(data)
        assert cd.export_dict() == data
