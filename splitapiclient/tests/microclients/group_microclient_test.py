from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import GroupMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestGroupMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = GroupMicroClient(sc)
        data = {'objects': [{
                'id': 'group_id1',
                'name': 'group_name1',
                'description': 'description',
                'type': 'group'
            }, {
                'id': 'group_id2',
                'name': 'group_name2',
                'description': 'description',
                'type': 'group'
            }],
            'offset': 1,
            'totalCount': 2,
            'limit': 2
        }

        SyncHttpClient.make_request.return_value = data
        result = emc.list()
        SyncHttpClient.make_request.assert_called_once_with(
            GroupMicroClient._endpoint['all_items'],
            offset = 0
        )
        data = [{
            'id': 'group_id1',
            'name': 'group_name1',
            'description': None,
            'type': None
        }, {
            'id': 'group_id2',
            'name': 'group_name2',
            'description': None,
            'type': None
        }]
        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]

    def test_create_group(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = GroupMicroClient(sc)
        data = {
            'name': 'gr1',
            'description':'desc'
        }
        response = {
            'id': 'group_id',
            'name': 'gr1',
            'description': None,
            'type': None
        }
        SyncHttpClient.make_request.return_value = response
        
        result = emc.create_group(data)
        SyncHttpClient.make_request.assert_called_once_with(
            GroupMicroClient._endpoint['create_group'],
            body = data
        )
        assert result.to_dict() == response

    def test_delete_group(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = GroupMicroClient(sc)
        SyncHttpClient.make_request.return_value = True
        
        result = emc.delete_group('group1')
        SyncHttpClient.make_request.assert_called_once_with(
            GroupMicroClient._endpoint['delete_group'],
            groupId = 'group1'
        )
        assert result == True

    def test_update_group(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = GroupMicroClient(sc)
        data = {
            'name': 'gr1',
            'description':'desc'
        }
        response = {
            'id': 'group1',
            'name': 'gr1',
            'description': 'desc',
            'type': 'group'
        }
        SyncHttpClient.make_request.return_value = response
        
        result = emc.update_group('group1', data)
        SyncHttpClient.make_request.assert_called_once_with(
            GroupMicroClient._endpoint['update_group'],
            groupId = 'group1',
            body = data
        )
        attr = {
            'id': result._id,
            'name': result._name,
            'description': result._description,
            'type': 'group'
        }
        assert attr == response
