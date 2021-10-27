from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import Attribute
from splitapiclient.microclients import AttributeMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client


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
            'splitapiclient.resources.base_resource.BaseResource.__init__',
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
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(tt, data['id'], client)
        assert data['displayName'] == tt.display_name
        assert data['trafficTypeId'] == tt.traffic_type_id
        assert data['description'] == tt.description
        assert data['dataType'] == tt.data_type

    def test_getters_and_setters(self):
        '''
        '''
        attr1 = Attribute()
        attr1.id = 'a'
        attr1.traffic_type_id = 'b'
        attr1.display_name = 'c'
        attr1.description = 'd'
        attr1.data_type = 'e'

        assert attr1.id == 'a'
        assert attr1.traffic_type_id == 'b'
        assert attr1.display_name == 'c'
        assert attr1.description == 'd'
        assert attr1.data_type == 'e'


    def test_save(self, mocker):
        '''
        '''
        attr_data = {
            'id': '1',
            'displayName': 'n1',
            'description': 'asd',
            'trafficTypeId': '111',
            'dataType': 'string',
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = attr_data
        a1 = Attribute(attr_data, http_client_mock)

        res = a1.save()

        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['create'],
            attr_data,
            trafficTypeId=a1.traffic_type_id,
            workspaceId=None
        )
        attr_data['isSearchable']=None
        attr_data['workspaceId']=None
        assert res.to_dict() == attr_data

        attr_data = {
            'id': '1',
            'displayName': 'n1',
            'description': 'asd',
            'trafficTypeId': '111',
            'dataType': 'string',
        }
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = attr_data
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        a2 = Attribute(attr_data)
        res = a2.save(ic)
        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['create'],
            attr_data,
            trafficTypeId=a2.traffic_type_id,
            workspaceId=None
        )
        attr_data['isSearchable']=None
        attr_data['workspaceId']=None
        assert res.to_dict() == attr_data

    def test_delete(self, mocker):
        '''
        '''
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = None
        a1 = Attribute(
            {
                'id': '1',
                'name': 'n1',
                'description': 'asd',
                'trafficTypeId': '111',
                'dataType': 'string',
                'isSearchable': False,
                'workspaceId': None
            },
            http_client_mock
        )

        res = a1.delete()

        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['delete'],
            trafficTypeId=a1.traffic_type_id,
            attributeId=a1.id,
            workspaceId=None
        )

        assert res is None

        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = None
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        a2 = Attribute({
            'id': '1',
            'name': 'n1',
            'description': 'asd',
            'trafficTypeId': '111',
            'dataType': 'string',
            'isSearchable': False,
            'workspaceId': None
        })
        res = a2.delete(ic)
        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['delete'],
            trafficTypeId=a2.traffic_type_id,
            attributeId=a2.id,
            workspaceId=None
        )
        assert res is None
