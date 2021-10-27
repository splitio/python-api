from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources.treatment import Treatment

class TestTreatment:
    '''
    Tests for the Treatment class' methods
    '''
    def test_constructor(self):
        '''
        '''
        data = {
            'name': 'tr1',
            'configurations': '{}',
            'description': 'desc',
            'keys': [ 'key1' ],
            'segments': [ 'seg1' ]
        }
        tr = Treatment(data)
        assert tr.export_dict() == data
