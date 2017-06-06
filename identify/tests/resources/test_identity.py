from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from identify.resources.identity import Identity
from identify.http_clients.sync_client import SyncHttpClient
from identify.util.exceptions import MethodNotApplicable


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
            'identify.resources.base_resource.BaseResource.__init__',
            new=mock_init
        )
        env = Identity(client, 'key', 'ttid', 'envid', 'vals')
        from identify.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(env, client, 'key')

    def test_build_single_from_collection_response(self):
        '''
        '''
        client = object()
        with pytest.raises(MethodNotApplicable):
            Identity._build_single_from_collection_response(
                client,
                {
                    'key': 'key',
                    'ttid': 'ttid',
                    'envid': 'envid',
                    'vals': 'vals'
                }
            )

    def test_create(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        Identity.create(sc, 'key', '123', '456', {'asd': 1})
        SyncHttpClient.make_request.assert_called_once_with(
            Identity._endpoint['create'],
            {
                'key': 'key',
                'trafficTypeId': '123',
                'environmentId': '456',
                'values': {'asd': 1},
            },
            trafficTypeId='123',
            environmentId='456',
            key='key'
        )

    def test_create_many(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        entities = {
            'key1': { 'asd': 1},
            'key2': { 'asd': 2},
        }
        Identity.create_many(sc, '123', '456', entities)
        SyncHttpClient.make_request.assert_called_once_with(
            Identity._endpoint['create_many'],
            [{
                'key': 'key2',
                'trafficTypeId': '123',
                'environmentId': '456',
                'values': {'asd': 2},

            },
            {
                'key': 'key1',
                'trafficTypeId': '123',
                'environmentId': '456',
                'values': {'asd': 1},
            }],
            trafficTypeId='123',
            environmentId='456',
        )

    def test_update(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        Identity.update(sc, 'key', '123', '456', {'asd': 1})
        SyncHttpClient.make_request.assert_called_once_with(
            Identity._endpoint['update'],
            {
                'key': 'key',
                'trafficTypeId': '123',
                'environmentId': '456',
                'values': {'asd': 1},
            },
            trafficTypeId='123',
            environmentId='456',
            key='key'
        )

    def test_patch(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        Identity.patch(sc, 'key', '123', '456', {'asd': 1})
        SyncHttpClient.make_request.assert_called_once_with(
            Identity._endpoint['patch'],
            {
                'key': 'key',
                'trafficTypeId': '123',
                'environmentId': '456',
                'values': {'asd': 1},
            },
            trafficTypeId='123',
            environmentId='456',
            key='key'
        )

    def test_delete_all_attributes(self, mocker):
        '''
        '''
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        Identity.delete_all_attributes(sc, '123', '456', 'key')
        SyncHttpClient.make_request.assert_called_once_with(
            Identity._endpoint['delete_attributes'],
            trafficTypeId='123',
            environmentId='456',
            key='key'
        )

    def test_update_this(self, mocker):
        '''
        '''
        mocker.patch('identify.resources.identity.Identity.update')
        sc = SyncHttpClient('abc', 'abc')
        attr = Identity(sc, 'key', '123', '456', {'asd': '1'})
        attr.update_this({'asd':'2'})
        Identity.update.assert_called_once_with(
            sc,
            'key',
            '123',
            '456',
            {'asd': '2'}
        )

    def test_patch_this(self, mocker):
        '''
        '''
        mocker.patch('identify.resources.identity.Identity.patch')
        sc = SyncHttpClient('abc', 'abc')
        attr = Identity(sc, 'key', '123', '456', {'asd': '1'})
        attr.patch_this({'qwe':'3'})
        Identity.patch.assert_called_once_with(
            sc,
            'key',
            '123',
            '456',
            {'qwe': '3'}
        )

    def test_delete_attributes_this(self, mocker):
        '''
        '''
        mocker.patch('identify.resources.identity.Identity.delete_all_attributes')
        sc = SyncHttpClient('abc', 'abc')
        attr = Identity(sc, 'key', '123', '456', {'asd': '1'})
        attr.delete_attributes_this()
        Identity.delete_all_attributes.assert_called_once_with(sc, '123', '456', 'key')
