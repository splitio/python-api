from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import SegmentDefinitionMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestSegmentDefinitionMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = SegmentDefinitionMicroClient(sc)
        data = {'objects': [{
                'name': 'name',
                'environment': {
                    'id': 'env_id',
                    'name': 'env'
                }},             {
                'name': 'name',
                'environment': {
                    'id': '1',
                    'name': 'env'
                }}
            ],
            'offset': 1,
            'totalCount': 2,
            'limit': 2
        }

        SyncHttpClient.make_request.return_value = data
        result = emc.list('env_id', 'ws_id')
        SyncHttpClient.make_request.assert_called_once_with(
            SegmentDefinitionMicroClient._endpoint['all_items'],
            workspaceId = 'ws_id',
            environmentId = 'env_id',
            offset = 0
        )
        data = [{
                'name': 'name',
                'environment': None,
                'creationTime': None,
                'trafficType': None
                }, {
                'name': 'name',
                'environment': None,
                'creationTime': None,
                'trafficType': None
                }
            ]

        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]
