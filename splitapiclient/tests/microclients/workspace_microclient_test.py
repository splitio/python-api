from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import WorkspaceMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestWorkspaceMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = WorkspaceMicroClient(sc)
        data = {'objects': [{
                    'id': 'ws1',
                    'name': 'Workspace 1',
                    'requiresTitleAndComments': 'string'
                    }, {
                    'id': 'ws2',
                    'name': 'Workspace 2'
                    }],
                'offset': 1,
                'totalCount': 2,
                'limit': 2
        }
        SyncHttpClient.make_request.return_value = data
        result = emc.list()
        SyncHttpClient.make_request.assert_called_once_with(
            WorkspaceMicroClient._endpoint['all_items'],
            offset = 0
        )
        data = [{
            'id': 'ws1',
            'name': 'Workspace 1',
            'requiresTitleAndComments': None
        }, {
            'id': 'ws2',
            'name': 'Workspace 2',
            'requiresTitleAndComments': None
        }]
        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]

    def test_delete(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = WorkspaceMicroClient(sc)
        SyncHttpClient.make_request.return_value = True
        result = emc.delete('ws_1')
        SyncHttpClient.make_request.assert_called_once_with(
            WorkspaceMicroClient._endpoint['delete'],
            workspaceId = 'ws_1',
        )
        assert result == True

    def test_update(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = WorkspaceMicroClient(sc)
        data = {
            'id': 'ws1',
            'name': 'Workspace 1',
            'requiresTitleAndComments': None
        }
        SyncHttpClient.make_request.return_value = data
        result = emc.update('ws_1', 'name', 'ws_new')
        body_data = [{'op': 'replace', 'path': '/name', 'value': 'ws_new'}]
        SyncHttpClient.make_request.assert_called_once_with(
            WorkspaceMicroClient._endpoint['update'],
            body = body_data,
            workspaceId = 'ws_1',
        )
        response = {
            'id': 'ws1',
            'name': 'Workspace 1',
            'requiresTitleAndComments': None
        }
        assert response == result.to_dict()


    def test_add(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = WorkspaceMicroClient(sc)
        data = {
            'id': 'ws1',
            'name': 'Workspace 1',
            'requiresTitleAndComments': None
        }
        SyncHttpClient.make_request.return_value = data
        result = emc.add(data)
        SyncHttpClient.make_request.assert_called_once_with(
            WorkspaceMicroClient._endpoint['create'],
            body = data,
        )
        response = {
            'id': 'ws1',
            'name': 'Workspace 1',
            'requiresTitleAndComments': None
        }
        assert response == result.to_dict()
