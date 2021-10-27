from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import Segment
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client
from splitapiclient.microclients import SegmentMicroClient

class TestSegment:
    '''
    Tests for the Segment class' methods
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
        seg = Segment(
            {
                'name': 'name',
                'description': '1',
                'workspaceId': 'ws_id'
            },
            client
        )
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(seg, 'name', client)

    def test_getters_and_setters(self):
        '''
        '''
        ws1 = Segment(
        {
            'name': 'name',
            'description': '1',
        })
        assert ws1.name == 'name'
        assert ws1.description == '1'

    def test_add_to_environment(self, mocker):
        '''
        '''
        data = {
            'name': 'name',
            'description': '1',
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        seg = Segment(
            {
                'name': 'name',
                'description': '1',
                'workspaceId': None
            },
            http_client_mock
        )
        attr = seg.add_to_environment('env_id')

        data = {
            'name': 'name',
        }
        http_client_mock.make_request.assert_called_once_with(
            SegmentMicroClient._endpoint['add_to_environment'],
            body = "",
            segmentName = 'name',
            environmentId = 'env_id'
        )
        data['creationTime'] = None
        data['trafficType'] = None
        data['environment'] = None
        assert attr.to_dict() == data

    def test_remove_from_environment(self, mocker):
        '''
        '''
        environment_id = 'e1'
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        seg = Segment(
            {
                'name': 'name',
                'description': '1',
                'workspaceId': None
            },
            http_client_mock
        )
        attr = seg.remove_from_environment(environment_id)

        http_client_mock.make_request.assert_called_once_with(
            SegmentMicroClient._endpoint['remove_from_environment'],
            body="",
            segmentName = 'name',
            environmentId = environment_id
        )
        assert attr == True
