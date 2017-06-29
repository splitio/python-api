from __future__ import absolute_import, division, print_function, \
    unicode_literals

from identify.microclients import EnvironmentMicroClient
from identify.http_clients.sync_client import SyncHttpClient


class TestEnvironmentMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = EnvironmentMicroClient(sc)
        data = [{
            'id': '123',
            'name': 'env1'
        }, {
            'id': '124',
            'name': 'env2'
        }]
        SyncHttpClient.make_request.return_value = data
        result = emc.list()
        SyncHttpClient.make_request.assert_called_once_with(
            EnvironmentMicroClient._endpoint['all_items']
        )
        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]
