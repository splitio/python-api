from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources.rule import Rule

class TestRule:
    '''
    Tests for Rule, Condition and Matcher classes
    '''
    def test_constructor(self):
        '''
        '''
        data = {
            'condition': {
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
            },
            'buckets': [{
                'treatment': 'on',
                'size': 50
            },{
                'treatment': 'off',
                'size': 50
            }]
        }
        rl = Rule(data)
        assert rl.export_dict() == data
