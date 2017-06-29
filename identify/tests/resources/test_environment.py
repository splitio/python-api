from __future__ import absolute_import, division, print_function, \
    unicode_literals

from identify.resources import Environment
from identify.microclients import IdentityMicroClient
from identify.http_clients.sync_client import SyncHttpClient
from identify.main import get_client


class TestEnvironment:
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
        env = Environment(
            {
                'id': '123',
                'name': 'name'
            },
            client
        )
        from identify.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(env, '123', client)

    def test_add_identity(self, mocker):
        '''
        '''
        data = {
            'key': 'key1',
            'trafficTypeId': '1',
            'environmentId': '1',
            'values': {'a1': 'v1'},
            'organizationId': 'o1',
        }
        http_client_mock = mocker.Mock()
        http_client_mock.make_request.return_value = data
        tt1 = Environment(
            {
                'id': '1',
                'name': 'e1',
            },
            http_client_mock
        )

        attr = tt1.add_identity(data)

        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
            environmentId=data['environmentId'],
            key=data['key']
        )
        assert attr.to_dict() == data

        tt2 = Environment(
            {
                'id': '1',
                'name': 'e2',
            },
        )

        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = data
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        attr = tt2.add_identity(data, ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
            environmentId=data['environmentId'],
            key=data['key']
        )
        assert attr.to_dict() == data

    def test_add_identities(self, mocker):
        '''
        '''
        data = [{
            'key': 'key1',
            'trafficTypeId': '1',
            'environmentId': '1',
            'values': {'a1': 'v1'},
            'organizationId': 'o1',
        }, {
            'key': 'key2',
            'trafficTypeId': '1',
            'environmentId': '1',
            'values': {'a2': 'v2'},
            'organizationId': 'o1',
        }]

        http_client_mock = mocker.Mock()
        http_client_mock.make_request.return_value = {
            'objects': data,
            'failed': [],
            'metadata': {}
        }
        tt1 = Environment(
            {
                'id': '1',
                'name': 'e1',
            },
            http_client_mock
        )

        s1, f1 = tt1.add_identities(data)

        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            data,
            trafficTypeId=data[0]['trafficTypeId'],
            environmentId=data[0]['environmentId'],
        )
        assert [s.to_dict() for s in s1] == data

        tt2 = Environment(
            {
                'id': '1',
                'name': 'e2',
            },
        )

        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = {
            'objects': data,
            'failed': [],
            'metadata': {}
        }
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        s2, f2 = tt2.add_identities(data, ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            data,
            trafficTypeId=data[0]['trafficTypeId'],
            environmentId=data[0]['environmentId'],
        )
        assert [s.to_dict() for s in s2] == data
