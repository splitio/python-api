from __future__ import absolute_import, division, print_function, \
    unicode_literals

from identify.resources.environment import Environment


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
        env = Environment(client, '123', 'name')
        from identify.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(env, client, '123')

    def test_build_single_from_collection_response(self, mocker):
        '''
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'identify.resources.environment.Environment.__init__',
            new=mock_init
        )
        Environment.__init__.return_value = None
        Environment._build_single_from_collection_response(
            client,
            {
                'id': '123',
                'name': 'name',
            }
        )
        Environment.__init__.assert_called_once_with(
            client,
            '123',
            'name',
        )
