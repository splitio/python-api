from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import WorkspaceMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestWorkspaceMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = WorkspaceMicroClient(sc)
        data = {'objects': [{
                    'id': 'ws1',
                    'name': 'Workspace 1',
                    }, {
                    'id': 'ws2',
                    'name': 'Workspace 2'
                    }],
                'offset': 1,
                'totalCount': 2,
                'limit': 2
        }
        SyncHttpClient.make_request.return_value = data
        result = emc.list()
        SyncHttpClient.make_request.assert_called_once_with(
            WorkspaceMicroClient._endpoint['all_items'],
            offset = 0
        )
        data = [{
            'id': 'ws1',
            'name': 'Workspace 1',
        }, {
            'id': 'ws2',
            'name': 'Workspace 2',
        }]
        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]
