from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources.base_resource import BaseResource


class TestBaseResource:
    '''
    Tests for the BaseResource class' methods
    '''

    def test_constructor(self):
        '''
        '''
        class SampleResource(BaseResource):
            pass

        with pytest.raises(TypeError):
            SampleResource('', '')

        class SampleResource2(BaseResource):
            _endpoint = {}
            _schema = {}
            def from_dict(self, c, r): pass

        b = SampleResource2('', '')
        assert isinstance(b, BaseResource)
