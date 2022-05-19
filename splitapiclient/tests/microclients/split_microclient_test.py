from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import SplitMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestSplitMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = SplitMicroClient(sc)
        data = {'objects': [{
                'name': 'sp1',
                'description': 'desc',
                'creationTime' : None,
                'id': None,
                'rolloutStatus': None,
                'rolloutStatusTimestamp': None,
                'tags': None,
                'owners': None
            }, {
                'name': 'sp2',
                'description': 'desc',
                'creationTime' : None,
                'id': None,
                'rolloutStatus': None,
                'rolloutStatusTimestamp': None,
                'tags': None,
                'owners': None
            }],
            'offset': 1,
            'totalCount': 2,
            'limit': 2
        }

        SyncHttpClient.make_request.return_value = data
        result = emc.list('ws_id', ['tag1', 'tag2'])
        tags_list = ""
        for tag in ['tag1', 'tag2']:
            tags_list = tags_list + "&tag=" + tag
        SyncHttpClient.make_request.assert_called_once_with(
            SplitMicroClient._endpoint['all_items'],
            workspaceId = 'ws_id',
            offset = 0,
            tags = tags_list
        )
        data = [{
            'name': 'sp1',
            'description': 'desc',
            'trafficType' : None,
            'creationTime' : None,
            'id': 'sp1',
            'rolloutStatus': None,
            'rolloutStatusTimestamp': None,
            'tags': None,
            'owners': None,
            'id': None
        }, {
            'name': 'sp2',
            'description': 'desc',
            'trafficType' : None,
            'creationTime' : None,
            'id': 'sp2',
            'rolloutStatus': None,
            'rolloutStatusTimestamp': None,
            'tags': None,
            'owners': None,
            'id': None
        }]

        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]

    def test_get(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = SplitMicroClient(sc)
        data = {
            'name': 'sp1',
            'description': 'desc',
            'creationTime' : None,
            'id': None,
            'rolloutStatus': None,
            'rolloutStatusTimestamp': None,
            'tags': None,
            'owners': None
        }

        SyncHttpClient.make_request.return_value = data
        result = emc.get('sp1', 'ws_id')
        SyncHttpClient.make_request.assert_called_once_with(
            SplitMicroClient._endpoint['get'],
            workspaceId = 'ws_id',
            splitName = 'sp1'
        )
        data = {
            'name': 'sp1',
            'description': 'desc',
            'trafficType' : None,
            'creationTime' : None,
            'id': 'sp1',
            'rolloutStatus': None,
            'rolloutStatusTimestamp': None,
            'tags': None,
            'owners': None,
            'id': None
        }
        assert result.to_dict() == data
