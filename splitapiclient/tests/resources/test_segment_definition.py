from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import SegmentDefinition
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client
from splitapiclient.microclients import SegmentDefinitionMicroClient
from splitapiclient.microclients import ChangeRequestMicroClient
class TestSegmentDefinition:
    '''
    Tests for the SegmentDefinition class' methods
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
        seg = SegmentDefinition(
            {
                'name': 'name',
                'environment': {
                    'id': '1',
                    'name': 'env'
                },
            },
            client
        )
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(seg, 'name', client)

    def test_getters_and_setters(self):
        '''
        '''
        seg1 = SegmentDefinition(
            {
                'name': 'name',
                'environment': {
                    'id': '1',
                    'name': 'env'
                },
                'trafficType': {},
            })
        assert seg1.name == 'name'

    def test_get_keys(self, mocker):
        '''
        '''
        data = {
            'keys': [{'key':'key1'}, {'key':'key2'}],
            'offset': 1,
            'count': 2,
            'limit': 2
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        seg = SegmentDefinition(
            {
                'name': 'name',
                'environment': {
                    'id': '1',
                    'name': 'env'
                },
                'trafficType': {},
            },
            http_client_mock
        )
        attr = seg.get_keys()

        data = ['key1', 'key2']
        http_client_mock.make_request.assert_called_once_with(
            SegmentDefinitionMicroClient._endpoint['get_keys'],
            environmentId = '1',
            segmentName = 'name',
            offset = 0
        )
        assert attr == data

    def test_import_keys_from_json(self, mocker):
        '''
        '''
        data = {"keys":["id1", "id2"], "comment":"a comment"}
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        seg = SegmentDefinition(
            {
                'name': 'name',
                'environment': {
                    'id': '1',
                    'name': 'env'
                },
                'trafficType': {},
            },
            http_client_mock
        )
        attr = seg.import_keys_from_json(False, data)

        http_client_mock.make_request.assert_called_once_with(
            SegmentDefinitionMicroClient._endpoint['import_from_json'],
            body=data,
            environmentId = '1',
            segmentName = 'name',
            replaceKeys = False
        )
        assert attr == True

    def test_remove_keys(self, mocker):
        '''
        '''
        data = {"keys":["id1", "id2"], "comment":"a comment"}
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        seg = SegmentDefinition(
            {
                'name': 'name',
                'environment': {
                    'id': '1',
                    'name': 'env'
                },
                'trafficType': {},
            },
            http_client_mock
        )
        attr = seg.remove_keys(data)

        http_client_mock.make_request.assert_called_once_with(
            SegmentDefinitionMicroClient._endpoint['remove_keys'],
            body=data,
            environmentId = '1',
            segmentName = 'name',
        )
        assert attr == True

    def test_submit_change_request(self, mocker):
        '''
        '''
        data = {
            'segment': {
                'name': 'segment1',
                'keys': [],
            },
            'title': 'title',
            'operationType': 'op',
            'comment': 'com',
            'approvers': ['approver'],
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        seg = SegmentDefinition(
            {
                'name': 'segment1',
                'environment': {
                    'id': 'env_id',
                    'name': 'env'
                },
                'trafficType': {},
            },
            http_client_mock
        )
        definition = []

        attr = seg.submit_change_request(definition, 'op', 'title', 'com', ['approver'], None, 'ws_id')

        http_client_mock.make_request.assert_called_once_with(
            ChangeRequestMicroClient._endpoint['submit_change_request'],
            workspaceId = 'ws_id',
            environmentId = 'env_id',
            body = data
        )
        data1 = {
            'split': None,
            'segment': None,
            'id': None,
            'status': None,
            'title': None,
            'comment': None,
            'approvers': None,
            'operationType': None,
            'comments': None,
            'rolloutStatus': None
        }

        assert attr.to_dict() == data1
