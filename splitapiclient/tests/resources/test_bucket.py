from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources.bucket import Bucket

class TestBucket:
    '''
    Tests for the Bucket class' methods
    '''
    def test_constructor(self):
        '''
        '''
        data = {
            'treatment': 'tr1',
            'size': 100
        }
        bk = Bucket(data)
        assert bk.export_dict() == data
