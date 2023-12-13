from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.main.sync_apiclient import SyncApiClient
from splitapiclient.util.exceptions import InsufficientConfigArgumentsException

class TestSyncApiClient:
    '''
    '''

    def test_constructor(self):
        '''
        '''
        # Should have PROD url by default
        c1 = SyncApiClient({'apikey': '123'})
        assert c1._base_url == SyncApiClient.BASE_PROD_URL
        assert c1._apikey == '123'

        # Should fail if no apikey propvided
        with pytest.raises(InsufficientConfigArgumentsException):
            c2 = SyncApiClient({})

        # Should override url if passed
        c3 = SyncApiClient({'base_url': 'http://test', 'apikey': '123'})
        assert c3._base_url == 'http://test'
        assert c3._apikey == '123'
