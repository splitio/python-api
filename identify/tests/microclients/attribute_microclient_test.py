from __future__ import absolute_import, division, print_function, \
    unicode_literals

from identify.microclients import AttributeMicroClient
from identify.http_clients.sync_client import SyncHttpClient


class TestAttributeMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        amc = AttributeMicroClient(sc)
        data = [{
            'id': '123',
            'trafficTypeId': '456',
            'displayName': 'name',
            'description': 'desc',
            'dataType': 'dt',
            'isSearchable': False
        }, {
            'id': '124',
            'trafficTypeId': '456',
            'displayName': 'name',
            'description': 'desc',
            'dataType': 'dt',
            'isSearchable': False
        }]
        SyncHttpClient.make_request.return_value = data
        result = amc.list('456')
        SyncHttpClient.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['all_items'],
            trafficTypeId='456'
        )
        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]

    def test_create(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        amc = AttributeMicroClient(sc)
        data = {
            'id': '123',
            'trafficTypeId': '456',
            'displayName': 'name',
            'description': 'desc',
            'dataType': 'dt',
            'isSearchable': False
        }
        amc.create(data)
        SyncHttpClient.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['create'],
            data,
            trafficTypeId='456'
        )

    def test_delete(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        amc = AttributeMicroClient(sc)
        amc.delete_by_id('123', '456')
        sc.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['delete'],
            attributeId='123',
            trafficTypeId='456'
        )
