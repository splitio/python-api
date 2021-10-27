from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import Group
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client
from splitapiclient.microclients import GroupMicroClient

class TestGroup:
    '''
    Tests for the Group class' methods
    '''
    def test_constructor(self, mocker):
        '''
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'splitapiclient.resources.base_resource.BaseResource.__init__',
            new=mock_init
        )
        gr1 = Group({
                'id': 'id',
                'type': 'group',
                'name': 'gr',
                'description': 'string'
            },
            client
        )
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(gr1, 'id', client)

    def test_getters_and_setters(self):
        '''
        '''
        gr1 = Group({
                'id': 'id',
                'type': 'group',
                'name': 'gr',
                'description': 'string'
            }
        )
        assert gr1.name == 'gr'
