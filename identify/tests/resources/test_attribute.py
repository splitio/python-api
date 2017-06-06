from __future__ import absolute_import, division, print_function, \
    unicode_literals

from identify.resources.attribute import Attribute
from identify.clients.sync_client import SyncHttpClient


class TestTrafficType:
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
        tt = Attribute(client, '123', '456', 'display_name', 'desc', 'dt')
        from identify.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(tt, client, '123')

    def test_build_single_from_collection_response(self, mocker):
        '''
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'identify.resources.attribute.Attribute.__init__',
            new=mock_init
        )
        Attribute.__init__.return_value = None
        Attribute._build_single_from_collection_response(
            client,
            {
                'id': '123',
                'trafficTypeId': '456',
                'displayName': 'name',
                'description': 'desc',
                'dataType': 'dt',
            }
        )
        Attribute.__init__.assert_called_once_with(
            client,
            '123',
            '456',
            'name',
            'desc',
            'dt'
        )

    def test_create(self, mocker):
        '''
        '''
        mocker.patch('identify.clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        Attribute.create(sc, '123', '456', 'name', 'desc', 'dt')
        SyncHttpClient.make_request.assert_called_once_with(
            Attribute._endpoint['create'],
            {
                'id': '123',
                'trafficTypeId': '456',
                'displayName': 'name',
                'description': 'desc',
                'dataType': 'DT'
            },
            trafficTypeId='456'
        )

    def test_delete(self, mocker):
        '''
        '''
        mocker.patch('identify.clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        Attribute.delete(sc, '123', '456')
        sc.make_request.assert_called_once_with(
            Attribute._endpoint['delete'],
            attributeId='123',
            trafficTypeId='456'
        )

    def test_delete_this(self, mocker):
        '''
        '''
        mocker.patch('identify.resources.attribute.Attribute.delete')
        sc = SyncHttpClient('abc', 'abc')
        attr = Attribute(sc, '123', '456', 'name', 'desc', 'dt')
        attr.delete_this()
        Attribute.delete.assert_called_once_with(
            sc,
            '123',
            '456'
        )
