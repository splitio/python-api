from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import TrafficTypeMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestTrafficTypeMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        ttmc = TrafficTypeMicroClient(sc)
        data = [{
            'id': '123',
            'name': 'name1',
            'displayAttributeId': 'a1',
        }, {
            'id': '124',
            'name': 'name2',
            'displayAttributeId': 'a2',
        }]
        SyncHttpClient.make_request.return_value = data
        result = ttmc.list('ws_id')
        SyncHttpClient.make_request.assert_called_once_with(
            TrafficTypeMicroClient._endpoint['all_items'],
            workspaceId = 'ws_id'
        )
        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]
