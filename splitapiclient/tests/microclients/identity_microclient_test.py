from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import IdentityMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources import Identity
from splitapiclient.util.bulk_result import BulkOperationResult

class TestIdentityMicroClient:
    '''
    '''

    def test_create(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')

        data = {
            'key': 'key',
            'trafficTypeId': '123',
            'environmentId': '456',
            'values': {'asd': 1},
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
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        imc = IdentityMicroClient(sc)

        identities = [{
            'key': 'key1',
            'trafficTypeId': '123',
            'environmentId': '456',
            'values': {'asd': 1},
        }, {
            'key': 'key2',
            'trafficTypeId': '123',
            'environmentId': '456',
            'values': {'asd': 2},
        }]

        SyncHttpClient.make_request.return_value = {
            'objects': identities,
            'failed': [],
            'metadata': {},
        }
        result = imc.save_all(identities)
        assert isinstance(result, BulkOperationResult)
        assert [i.to_dict() for i in result.successful] == identities
        assert isinstance(result.failed, list)
        assert isinstance(result.metadata, dict)

        SyncHttpClient.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            identities,
            trafficTypeId=identities[0]['trafficTypeId'],
            environmentId=identities[0]['environmentId'],
        )


    def test_update(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')

        data = {
            'key': 'key',
            'trafficTypeId': '123',
            'environmentId': '456',
            'values': {'asd': 1},
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
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')

        data = {
            'key': 'key',
            'trafficTypeId': '123',
            'environmentId': '456',
            'values': {'asd': 1},
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

    def test_delete(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        imc = IdentityMicroClient(sc)
        imc.delete('123', '456', 'key')
        SyncHttpClient.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['delete_attributes'],
            trafficTypeId='123',
            environmentId='456',
            key='key'
        )

    def test_delete_by_instance(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        imc = IdentityMicroClient(sc)
        imc.delete_by_instance(Identity({
            'trafficTypeId': '123',
            'environmentId': '456',
            'key': 'key'
        }))
        SyncHttpClient.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['delete_attributes'],
            trafficTypeId='123',
            environmentId='456',
            key='key'
        )
