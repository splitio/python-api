from __future__ import absolute_import, division, print_function, \
    unicode_literals

from identify.resources.attribute import Attribute
from identify.microclients import AttributeMicroClient
from identify.http_clients.sync_client import SyncHttpClient
from identify.main import get_client


class TestAttribute:
    '''
    Tests for the TrafficType class' methods
    '''
    def test_constructor(self, mocker):
        '''
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'identify.resources.base_resource.BaseResource.__init__',
            new=mock_init
        )

        data = {
            'id': '123',
            'trafficTypeId': '456',
            'displayName': 'display_name',
            'description': 'desc',
            'dataType': 'dt',
            'isSearchable': False,
        }
        tt = Attribute(data, client)
        from identify.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(tt, data['id'], client)
        assert data['displayName'] == tt.display_name
        assert data['trafficTypeId'] == tt.traffic_type_id
        assert data['description'] == tt.description
        assert data['dataType'] == tt.data_type

    def test_delete(self, mocker):
        '''
        '''
        '''
        '''
        http_client_mock = mocker.Mock()
        http_client_mock.make_request.return_value = None
        a1 = Attribute(
            {
                'id': '1',
                'name': 'n1',
                'description': 'asd',
                'trafficTypeId': '111',
                'dataType': 'string',
                'isSearchable': False,
            },
            http_client_mock
        )

        res = a1.delete()

        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['delete'],
            trafficTypeId=a1.traffic_type_id,
            attributeId=a1.id
        )

        assert res is None

        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = None
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        a2 = Attribute({
            'id': '1',
            'name': 'n1',
            'description': 'asd',
            'trafficTypeId': '111',
            'dataType': 'string',
            'isSearchable': False,
        })
        res = a2.delete(ic)
        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['delete'],
            trafficTypeId=a2.traffic_type_id,
            attributeId=a2.id
        )
        assert res is None
