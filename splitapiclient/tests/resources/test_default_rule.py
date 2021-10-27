from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources.default_rule import DefaultRule

class TestRule:
    '''
    Tests for the DefaultRule class' methods
    '''
    def test_constructor(self):
        '''
        '''
        data = {
            'treatment': 'tr1',
            'size': 100
        }
        dr = DefaultRule(data)
        assert dr.export_dict() == data
