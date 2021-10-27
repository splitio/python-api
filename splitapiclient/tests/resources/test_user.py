from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import User
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client
from splitapiclient.microclients import UserMicroClient

class TestUser:
    '''
    Tests for the User class' methods
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
        us1 = User({
                'id': 'id',
                'type': 'user',
                'name': 'us1',
                'email': 'email',
                'status': 'st',
                'groups': []
            },
            client
        )
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(us1, 'id', client)

    def test_getters_and_setters(self):
        '''
        '''
        us1 = User({
                'id': 'id',
                'type': 'user',
                'name': 'us1',
                'email': 'email',
                'status': 'st',
                'groups': []
        })
        assert us1.email == 'email'

    def test_update_user(self, mocker):
        '''
        '''
        data = {
          'id': 'user_id',
          'type': 'user',
          'name': 'user_name',
          'email': 'email',
          'status': 'ACTIVE',
          'groups': []
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        us1 = User(data,
            http_client_mock
        )
        attr = us1.update_user(data)

        http_client_mock.make_request.assert_called_once_with(
            UserMicroClient._endpoint['update_user'],
            userId = 'user_id',
            body = data
        )
        data = {
          'id': 'user_id',
          'type': None,
          'name': None,
          'email': 'email',
          'status': None,
          'groups': None
        }
        assert attr.to_dict() == data

    def test_update_user_group(self, mocker):
        '''
        '''
        data = {
            'id': 'user_id',
            'type': 'user',
            'name': 'user_name',
            'email': 'email',
            'status': 'ACTIVE',
            'groups': [{
                'type': 'group',
                'id': 'gr_id'
            }]
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        us1 = User(data,
            http_client_mock
        )
        attr = us1.update_user_group(data)
#        body = [{
#            'op': 'replace',
#            'path': '/groups/0',
#            'value': {'id': 'gr_id', 'type':'group'}
#        }]
        http_client_mock.make_request.assert_called_once_with(
            UserMicroClient._endpoint['update_user_group'],
            userId = 'user_id',
            body = data
        )
        data = {
          'id': 'user_id',
          'type': None,
          'name': None,
          'email': 'email',
          'status': None,
          'groups': None
        }
        assert attr.to_dict() == data
