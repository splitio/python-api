from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import UserMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestUserMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = UserMicroClient(sc)
        data = {'data': [{
                'id': 'id1',
                'type': 'string',
                'name': 'us1',
                'email': 'email1',
                'status': 'string',
                'groups': [],
            }, {
                'id': 'id2',
                'type': 'string',
                'name': 'us2',
                'email': 'email2',
                'status': 'string',
                'groups': [],
            }],
            'nextMarker': None,
            'previousMarker': None,
            'limit': 20,
            'count': 2
        }

        SyncHttpClient.make_request.return_value = data
        result = emc.list('status')
        SyncHttpClient.make_request.assert_called_once_with(
            UserMicroClient._endpoint['list_initial'],
            status = 'status'
        )
        data = [{
            'id': 'id1',
            'type': None,
            'name': None,
            'email': 'email1',
            'status': None,
            'groups': None,
        }, {
            'id': 'id2',
            'type': None,
            'name': None,
            'email': 'email2',
            'status': None,
            'groups': None,
        }]
        assert result[0].to_dict() == data[0]
        assert result[1].to_dict() == data[1]

    def test_invite_user(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = UserMicroClient(sc)
        data = {
            'email': 'email',
            'groups':[{'id':'group_id', 'type':'group'}]
        }
        SyncHttpClient.make_request.return_value = True
        
        result = emc.invite_user(data)
        SyncHttpClient.make_request.assert_called_once_with(
            UserMicroClient._endpoint['invite_user'],
            body = data
        )
        assert result == True

    def test_delete(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = UserMicroClient(sc)
        SyncHttpClient.make_request.return_value = True
        
        result = emc.delete('user1')
        SyncHttpClient.make_request.assert_called_once_with(
            UserMicroClient._endpoint['delete_invite'],
            userId = 'user1'
        )
        assert result == True

    def test_update_user(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = UserMicroClient(sc)
        data = {
            'name': 'name',
            'email': 'email',
            '2fa': False,
            'status':'ACTIVE'
        }
        SyncHttpClient.make_request.return_value = data
        
        result = emc.update_user('user1', data)
        SyncHttpClient.make_request.assert_called_once_with(
            UserMicroClient._endpoint['update_user'],
            userId = 'user1',
            body = data
        )
        data = {
          'id': None,
          'type': 'user',
          'name': 'name',
          'email': 'email',
          'status': 'ACTIVE',
          'groups': None
        }
        response = {
          'id': result._id,
          'type': 'user',
          'name': result._name,
          'email': result._email,
          'status': result._status,
          'groups': None
        }
        assert response == data
