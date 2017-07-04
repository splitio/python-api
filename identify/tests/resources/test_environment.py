from __future__ import absolute_import, division, print_function, \
    unicode_literals

from identify.resources import Environment
from identify.resources import Identity
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

    def test_getters_and_setters(self):
        '''
        '''
        env1 = Environment({})
        env1.id = 'a'
        env1.name = 'b'

        assert env1.id == 'a'
        assert env1.name == 'b'

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
        env1 = Environment(
            {
                'id': '1',
                'name': 'e1',
            },
            http_client_mock
        )

        attr = env1.add_identity(data)

        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
            environmentId=data['environmentId'],
            key=data['key']
        )
        assert attr.to_dict() == data

        # Test by passing an instance instead of dict data
        http_client_mock.reset_mock()
        idinstance = Identity(data)
        env1.add_identity(idinstance)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            idinstance.to_dict(),
            trafficTypeId=idinstance.traffic_type_id,
            environmentId=idinstance.environment_id,
            key=idinstance.key
        )
        assert attr.to_dict() == data

        env2 = Environment(
            {
                'id': '1',
                'name': 'e2',
            },
        )

        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = data
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        attr = env2.add_identity(data, ic)
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
        env1 = Environment(
            {
                'id': '1',
                'name': 'e1',
            },
            http_client_mock
        )

        s1, f1 = env1.add_identities(data)

        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            data,
            trafficTypeId=data[0]['trafficTypeId'],
            environmentId=data[0]['environmentId'],
        )
        assert [s.to_dict() for s in s1] == data

        # Test by passing an instances as well as raw dict data
        http_client_mock.reset_mock()
        idinstances = [Identity(data[0]), data[1]]
        ss, ff = env1.add_identities(idinstances)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            data,
            trafficTypeId=idinstances[0].traffic_type_id,
            environmentId=idinstances[0].environment_id,
        )
        assert [s.to_dict() for s in ss] == data

        env2 = Environment(
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
        s2, f2 = env2.add_identities(data, ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            data,
            trafficTypeId=data[0]['trafficTypeId'],
            environmentId=data[0]['environmentId'],
        )
        assert [s.to_dict() for s in s2] == data
