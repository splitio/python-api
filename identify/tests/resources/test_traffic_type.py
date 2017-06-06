from __future__ import absolute_import, division, print_function, \
    unicode_literals

from identify.resources.traffic_type import TrafficType


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
        tt = TrafficType(client, '123', 'name', 'display_name')
        from identify.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(tt, client, '123')

    def test_build_single_from_collection_response(self, mocker):
        '''
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'identify.resources.traffic_type.TrafficType.__init__',
            new=mock_init
        )
        TrafficType.__init__.return_value = None
        TrafficType._build_single_from_collection_response(
            client,
            {
                'id': '123',
                'name': 'name',
                'displayAttributeId': 'display_name',
            }
        )
        TrafficType.__init__.assert_called_once_with(
            client,
            '123',
            'name',
            'display_name'
        )

    def test_fetch_attributes(self, mocker):
        '''
        '''
        client = object()
        mocker.patch(
            'identify.resources.base_resource.BaseResource.retrieve_all'
        )
        from identify.resources.base_resource import BaseResource
        tt = TrafficType(client, '123', 'name', 'display_name')
        tt.fetch_attributes()
        BaseResource.retrieve_all.assert_called_once_with(
            client,
            trafficTypeId='123'
        )

    def test_add_attribute(self, mocker):
        '''
        '''
        client = object()
        mocker.patch(
            'identify.resources.attribute.Attribute.create'
        )
        from identify.resources.attribute import Attribute
        tt = TrafficType(client, '123', 'name', 'display_name')
        tt.add_attribute(
            '234',
            'attr_display_name',
            'attr_description',
            'attr_data_type'
        )
        Attribute.create.assert_called_once_with(
            client, '234', '123', 'attr_display_name', 'attr_description',
            'attr_data_type'
        )
