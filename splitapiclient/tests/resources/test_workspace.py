from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import Workspace
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client
from splitapiclient.microclients import EnvironmentMicroClient
from splitapiclient.microclients import SegmentMicroClient
from splitapiclient.microclients import SplitMicroClient
from splitapiclient.microclients import WorkspaceMicroClient

class TestWorkspace:
    '''
    Tests for the Workspace class' methods
    '''
    def test_constructor(self, mocker):
        '''
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'splitapiclient.resources.base_resource.BaseResource.__init__',
            new = mock_init
        )
        ws = Workspace(
            {
                'id': '1',
                'name': 'name',
                'requiresTitleAndComments': None
            },
            client
        )
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(ws, '1', client)

    def test_getters_and_setters(self):
        '''
        '''
        ws1 = Workspace(
        {
                'id': 'a',
                'name': 'b',
                'requiresTitleAndComments': None
        })
        assert ws1.name == 'b'

    def test_add_environment(self, mocker):
        '''
        '''
        data = {
            'id': '123',
            'name': 'env1',
            'production':None,
            'creationTime' : None,
            'dataExportPermissions' : None,
            'environmentType' : None,
            'workspaceIds' : None,
            'changePermissions' : None,
            'type': None,
            'orgId' : None,
            'status' : None
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        ws1 = Workspace(
            {
                'id': '1',
                'name': 'e1',
                'requiresTitleAndComments': None
            },
            http_client_mock
        )

        attr = ws1.add_environment(data)

        http_client_mock.make_request.assert_called_once_with(
            EnvironmentMicroClient._endpoint['create'],
            body = data,
            workspaceId = '1'
        )
        assert attr.to_dict() == data

    def test_delete_environment(self, mocker):
        '''
        '''
        environment_id = 'e1'
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        ws1 = Workspace(
            {
                'id': '1',
                'name': 'e1',
                'requiresTitleAndComments': None
            },
            http_client_mock
        )

        attr = ws1.delete_environment(environment_id)

        http_client_mock.make_request.assert_called_once_with(
            EnvironmentMicroClient._endpoint['delete'],
            workspaceId = '1',
            environmentId = environment_id,
        )
        assert attr == True

    def test_add_segment(self, mocker):
        '''
        '''
        data = {
            'name': '1',
            'description': 'e1',
            'creationTime' : None,
            'tags': None
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        ws1 = Workspace(
            {
                'id': '1',
                'name': 'e1',
                'requiresTitleAndComments': None
            },
            http_client_mock
        )
        attr = ws1.add_segment(data, 'traffictypename')

        http_client_mock.make_request.assert_called_once_with(
            SegmentMicroClient._endpoint['create'],
            body = data,
            workspaceId = '1',
            trafficTypeName = 'traffictypename'
        )
        data = {
            'name': '1',
            'description': 'e1',
            'creationTime' : None,
            'tags': None
        }
        data['trafficType'] = None
        data['workspaceId'] = None
        assert attr.to_dict() == data

    def test_delete_segment(self, mocker):
        '''
        '''
        segment_name = 'e1'
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        ws1 = Workspace(
            {
                'id': '1',
                'name': 'e1',
                'requiresTitleAndComments': None
            },
            http_client_mock
        )

        attr = ws1.delete_segment(segment_name)

        http_client_mock.make_request.assert_called_once_with(
            SegmentMicroClient._endpoint['delete'],
            workspaceId = '1',
            segmentName = segment_name,
        )
        assert attr == True

    def test_add_split(self, mocker):
        '''
        '''
        data = {
            'name': '1',
            'description': 'e1',
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        ws1 = Workspace(
            {
                'id': '1',
                'name': 'e1',
                'requiresTitleAndComments': None
            },
            http_client_mock
        )

        attr = ws1.add_split(data, 'traffictypename')

        http_client_mock.make_request.assert_called_once_with(
            SplitMicroClient._endpoint['create'],
            body = data,
            workspaceId = '1',
            trafficTypeName = 'traffictypename'
        )
        data = {
            'name': '1',
            'description': 'e1',
        }
        data['trafficType'] = None
        data['creationTime'] = None
        data['id'] = None
        data['rolloutStatus'] = None
        data['rolloutStatusTimestamp'] = None
        data['tags'] = None
        data['owners'] = None
        
        assert attr.to_dict() == data

    def test_delete_split(self, mocker):
        '''
        '''
        split_name = 'e1'
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        ws1 = Workspace(
            {
                'id': '1',
                'name': 'e1',
                'requiresTitleAndComments': None
            },
            http_client_mock
        )

        attr = ws1.delete_split(split_name)

        http_client_mock.make_request.assert_called_once_with(
            SplitMicroClient._endpoint['delete'],
            workspaceId = '1',
            splitName = split_name,
        )
        assert attr == True

    def test_get_rollout_statuses(self, mocker):
        '''
        '''
        data = {}
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        ws1 = Workspace(
            {
                'id': '1',
                'name': 'e1',
                'requiresTitleAndComments': None
            },
            http_client_mock
        )

        attr = ws1.get_rollout_statuses('1')

        http_client_mock.make_request.assert_called_once_with(
            WorkspaceMicroClient._endpoint['get_rollout_statuses'],
            workspaceId = '1',
        )
        assert attr == data
