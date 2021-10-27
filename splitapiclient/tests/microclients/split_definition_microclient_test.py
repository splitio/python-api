from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import SplitDefinitionMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestSplitDefinitionMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = SplitDefinitionMicroClient(sc)
        data = {'objects': [{
                'name': 'split1',
                'environment': {},
                'trafficType': {},
                'killed': False,
                'treatments': [],
                'defaultTreatment': 'off',
                'trafficAllocation': 100,
                'lastTrafficReceivedAt': 0,
                'rules': [],
                'defaultRule': [],
                'creationTime': 0,
                'lastUpdateTime': 0
            }, {
                'name': 'split2',
                'environment': {},
                'trafficType': {},
                'killed': False,
                'treatments': [],
                'defaultTreatment': 'off',
                'trafficAllocation': 100,
                'lastTrafficReceivedAt': 0,
                'rules': [],
                'defaultRule': [],
                'creationTime': 0,
                'lastUpdateTime': 0
            }],
            'offset': 1,
            'totalCount': 2,
            'limit': 2
        }

        SyncHttpClient.make_request.return_value = data
        result = emc.list('env_id', 'ws_id')
        SyncHttpClient.make_request.assert_called_once_with(
            SplitDefinitionMicroClient._endpoint['all_items'],
            workspaceId = 'ws_id',
            environmentId = 'env_id',
            offset = 0
        )
        data = [{
                'name': 'split1',
                'environment': None,
                'trafficType': None,
                'killed': None,
                'treatments': None,
                'defaultTreatment': None,
                'trafficAllocation': None,
                'rules': None,
                'defaultRule': None,
                'creationTime': None,
                'lastUpdateTime': None,
            }, {
                'name': 'split2',
                'environment': None,
                'trafficType': None,
                'killed': None,
                'treatments': None,
                'defaultTreatment': None,
                'trafficAllocation': None,
                'rules': None,
                'defaultRule': None,
                'creationTime': None,
                'lastUpdateTime': None,
            }]
        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]
