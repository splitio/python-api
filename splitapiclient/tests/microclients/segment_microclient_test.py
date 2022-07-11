from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import SegmentMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestSegmentMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = SegmentMicroClient(sc)
        data = {'objects': [{
                'name': 'seg1',
                'description': 'desc',
                'creationTime' : None,
                'tags': None
                }, {
                'name': 'seg1',
                'description': 'desc',
                'creationTime' : None,
                'tags': None
            }],
            'offset': 1,
            'totalCount': 2,
            'limit': 2
        }

        SyncHttpClient.make_request.return_value = data
        result = emc.list('ws_id')
        SyncHttpClient.make_request.assert_called_once_with(
            SegmentMicroClient._endpoint['all_items'],
            workspaceId = 'ws_id',
            offset = 0
        )
        data = [{
                'name': 'seg1',
                'description': 'desc',
                'trafficType': None,
                'workspaceId': None,
                'creationTime' : None,
                'tags': None
                }, {
                'name': 'seg1',
                'description': 'desc',
                'trafficType': None,
                'workspaceId': None,
                'creationTime' : None,
                'tags': None
        }]

        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]
