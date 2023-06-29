from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import AttributeMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources import Attribute

class TestAttributeMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        amc = AttributeMicroClient(sc)
        data = [{
            'id': '123',
            'trafficTypeId': '456',
            'displayName': 'name',
            'description': 'desc',
            'dataType': 'dt',
            'isSearchable': False,
            'workspaceId': None,
            'suggestedValues': []
        }, {
            'id': '124',
            'trafficTypeId': '456',
            'displayName': 'name',
            'description': 'desc',
            'dataType': 'dt',
            'isSearchable': False,
            'workspaceId': None,
            'suggestedValues': []
        }]
        SyncHttpClient.make_request.return_value = data
        result = amc.list('456', 'ws_id')
        SyncHttpClient.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['all_items'],
            trafficTypeId='456',
            workspaceId='ws_id'
        )
        data = [{
            'id': '123',
            'trafficTypeId': '456',
            'displayName': 'name',
            'description': 'desc',
            'dataType': 'dt',
            'isSearchable': False,
            'workspaceId': None,
            'suggestedValues': []
        }, {
            'id': '124',
            'trafficTypeId': '456',
            'displayName': 'name',
            'description': 'desc',
            'dataType': 'dt',
            'isSearchable': False,
            'workspaceId': None,
            'suggestedValues': []
        }]
        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]

    def test_save(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        amc = AttributeMicroClient(sc)
        data = {
            'id': '123',
            'trafficTypeId': '456',
            'displayName': 'name',
            'description': 'desc',
            'dataType': 'dt',
            'isSearchable': False,
            'workspaceId': 'ws_id',
            'suggestedValues': []
        }
        amc.save(Attribute(data))
        data = {
            'id': '123',
            'trafficTypeId': '456',
            'displayName': 'name',
            'description': 'desc',
            'dataType': 'dt',
            'suggestedValues': []
        }
        SyncHttpClient.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['create'],
            data,
            trafficTypeId = '456',
            workspaceId = 'ws_id'
        )

    def test_delete(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        amc = AttributeMicroClient(sc)
        amc.delete('123', None, '456')
        sc.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['delete'],
            attributeId='123',
            trafficTypeId='456',
            workspaceId=None
        )

    def test_delete_by_instance(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        amc = AttributeMicroClient(sc)
        amc.delete_by_instance(Attribute({
             'workspaceId': None,
             'id': '123',
             'trafficTypeId': '456',
        }))
        sc.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['delete'],
            attributeId='123',
            workspaceId=None,
            trafficTypeId='456',
        )
