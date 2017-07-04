from __future__ import absolute_import, division, print_function, \
    unicode_literals

from identify.microclients import IdentityMicroClient
from identify.http_clients.sync_client import SyncHttpClient


class TestIdentityMicroClient:
    '''
    '''

    def test_create(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')

        data = {
            'key': 'key',
            'trafficTypeId': '123',
            'environmentId': '456',
            'values': {'asd': 1},
            'organizationId': 'oo1',
        }

        sc = SyncHttpClient('abc', 'abc')
        imc = IdentityMicroClient(sc)
        SyncHttpClient.make_request.return_value = data
        result = imc.save(data)
        SyncHttpClient.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
            environmentId=data['environmentId'],
            key=data['key']
        )

        assert result.to_dict() == data

    def test_create_many(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        imc = IdentityMicroClient(sc)

        identities = [{
            'key': 'key1',
            'trafficTypeId': '123',
            'environmentId': '456',
            'values': {'asd': 1},
            'organizationId': 'oo1',
        }, {
            'key': 'key2',
            'trafficTypeId': '123',
            'environmentId': '456',
            'values': {'asd': 2},
            'organizationId': 'oo1',
        }]

        SyncHttpClient.make_request.return_value = {
            'objects': identities,
            'failed': [],
            'metadata': {},
        }
        result = imc.save_all(identities)

        SyncHttpClient.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            identities,
            trafficTypeId=identities[0]['trafficTypeId'],
            environmentId=identities[0]['environmentId'],
        )

    def test_update(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')

        data = {
            'key': 'key',
            'trafficTypeId': '123',
            'environmentId': '456',
            'values': {'asd': 1},
            'organizationId': 'oo1',
        }

        sc = SyncHttpClient('abc', 'abc')
        imc = IdentityMicroClient(sc)
        SyncHttpClient.make_request.return_value = data
        result = imc.update(data)
        SyncHttpClient.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['update'],
            data,
            trafficTypeId=data['trafficTypeId'],
            environmentId=data['environmentId'],
            key=data['key']
        )

        assert result.to_dict() == data

    def test_patch(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')

        data = {
            'key': 'key',
            'trafficTypeId': '123',
            'environmentId': '456',
            'values': {'asd': 1},
            'organizationId': 'oo1',
        }

        sc = SyncHttpClient('abc', 'abc')
        imc = IdentityMicroClient(sc)
        SyncHttpClient.make_request.return_value = data
        result = imc.patch(data)
        SyncHttpClient.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['patch'],
            data,
            trafficTypeId=data['trafficTypeId'],
            environmentId=data['environmentId'],
            key=data['key']
        )

        assert result.to_dict() == data

    def test_delete_all_attributes(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        imc = IdentityMicroClient(sc)
        imc.delete_all_attributes_by_id('123', '456', 'key')
        SyncHttpClient.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['delete_attributes'],
            trafficTypeId='123',
            environmentId='456',
            key='key'
        )


