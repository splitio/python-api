from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.resources import Identity
from splitapiclient.microclients import IdentityMicroClient
from splitapiclient.main import get_client

class TestIdentity:
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
        identity = Identity(
            {
                'key': 'key',
                'trafficTypeId': 'ttid',
                'enironmentId': 'envid',
                'values': 'vals'
            },
            client
        )
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(identity, None, client)

    def test_getters_and_setters(self):
        '''
        '''
        identity1 = Identity()
        identity1.id = 'a'
        identity1.key = 'b'
        identity1.traffic_type_id = 'c'
        identity1.environment_id = 'd'
        identity1.values = 'e'

        assert identity1.id == 'a'
        assert identity1.key == 'b'
        assert identity1.traffic_type_id == 'c'
        assert identity1.environment_id == 'd'
        assert identity1.values == 'e'

    def test_save(self, mocker):
        '''
        '''
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        i1 = Identity(
            {
                'key': 'key1',
                'trafficTypeId': '1',
                'environmentId': '1',
                'values': {'a1': 'v1'},
            },
            http_client_mock
        )
        http_client_mock.make_request.return_value = i1.to_dict()

        res = i1.save()

        http_client_mock.make_request.assert_called_once_with(
           IdentityMicroClient._endpoint['create'],
            i1.to_dict(),
            trafficTypeId=i1.traffic_type_id,
            environmentId=i1.environment_id,
            key=i1.key
        )

        assert res.to_dict() == i1.to_dict()

        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = i1.to_dict()
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        i2 = Identity(i1.to_dict())
        res = i2.save(ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            i1.to_dict(),
            trafficTypeId=i2.traffic_type_id,
            environmentId=i2.environment_id,
            key=i2.key
        )
        assert res.to_dict() == i2.to_dict()

    def test_update(self, mocker):
        '''
        '''
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        i1 = Identity(
            {
                'key': 'key1',
                'trafficTypeId': '1',
                'environmentId': '1',
                'values': {'a1': 'v1'},
            },
            http_client_mock
        )
        http_client_mock.make_request.return_value = i1.to_dict()

        res = i1.update()

        http_client_mock.make_request.assert_called_once_with(
           IdentityMicroClient._endpoint['update'],
            i1.to_dict(),
            trafficTypeId=i1.traffic_type_id,
            environmentId=i1.environment_id,
            key=i1.key
        )

        assert res.to_dict() == i1.to_dict()

        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = i1.to_dict()
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        i2 = Identity(i1.to_dict())
        res = i2.update(ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['update'],
            i1.to_dict(),
            trafficTypeId=i2.traffic_type_id,
            environmentId=i2.environment_id,
            key=i2.key
        )
        assert res.to_dict() == i2.to_dict()

    def test_delete(self, mocker):
        '''
        '''
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        i1 = Identity(
            {
                'key': 'key1',
                'trafficTypeId': '1',
                'environmentId': '1',
                'values': {'a1': 'v1'},
            },
            http_client_mock
        )
        http_client_mock.make_request.return_value = None

        res = i1.delete()

        http_client_mock.make_request.assert_called_once_with(
           IdentityMicroClient._endpoint['delete_attributes'],
            trafficTypeId=i1.traffic_type_id,
            environmentId=i1.environment_id,
            key=i1.key
        )

        assert res is None

        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = None
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        i2 = Identity(i1.to_dict())
        res = i2.delete(ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['delete_attributes'],
            trafficTypeId=i2.traffic_type_id,
            environmentId=i2.environment_id,
            key=i2.key
        )
        assert res is None
