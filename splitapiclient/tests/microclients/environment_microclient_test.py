from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import EnvironmentMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.util.helpers import as_dict

class TestEnvironmentMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = EnvironmentMicroClient(sc)
        data = [{
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
            'status' : None,
            'apiTokens' : None
        }]
        SyncHttpClient.make_request.return_value = data
        result = emc.list('ws_id')
        SyncHttpClient.make_request.assert_called_once_with(
            EnvironmentMicroClient._endpoint['all_items'],
            workspaceId = 'ws_id'
        )
        assert result[0].to_dict() == data[0]

    def test_delete(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = EnvironmentMicroClient(sc)
        SyncHttpClient.make_request.return_value = True
        
        result = emc.delete('env_1', 'ws_1')
        SyncHttpClient.make_request.assert_called_once_with(
            EnvironmentMicroClient._endpoint['delete'],
            workspaceId = 'ws_1',
            environmentId = 'env_1'
        )
        assert result == True

    def test_update(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = EnvironmentMicroClient(sc)
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
            'status' : None,
            'apiTokens' : None
        }
        SyncHttpClient.make_request.return_value = data
        result = emc.update('env_1', 'ws_1', 'name', 'env_new')
        body_data = [{'op': 'replace', 'path': '/name', 'value': 'env_new'}]
        SyncHttpClient.make_request.assert_called_once_with(
            EnvironmentMicroClient._endpoint['update'],
            body = body_data,
            workspaceId = 'ws_1',
            environmentId = 'env_1'
        )
        response = {
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
            'status' : None,
            'apiTokens' : None
        }
        assert response == result.to_dict()


    def test_add(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = EnvironmentMicroClient(sc)
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
            'status' : None,
            'apiTokens' : None
        }
        SyncHttpClient.make_request.return_value = data
        result = emc.add(data, 'ws_1')
        SyncHttpClient.make_request.assert_called_once_with(
            EnvironmentMicroClient._endpoint['create'],
            body = data,
            workspaceId = 'ws_1'
        )
        response = {
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
            'status' : None,
            'apiTokens' : None
        }
        assert response == result.to_dict()
