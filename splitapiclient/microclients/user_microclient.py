from splitapiclient.resources import User
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class UserMicroClient:
    '''
    '''
    _endpoint = {
        'invite_user': {
            'method': 'POST',
            'url_template': ('users'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'delete_invite': {
            'method': 'DELETE',
            'url_template': ('users/{userId}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'list_initial': {
            'method': 'GET',
            'url_template': 'users?limit=200&status={status}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'list_next': {
            'method': 'GET',
            'url_template': 'users?limit=200&after={after}&status={status}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'update_user': {
            'method': 'PUT',
            'url_template': ('users/{userId}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'update_user_group': {
            'method': 'PATCH',
            'url_template': ('users/{userId}'),
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
    }

    def __init__(self, http_client):
        '''
        Constructor
        '''
        self._http_client = http_client

    def list(self, status):
        '''
        Returns a list of Users objects.

        :returns: list of User objects
        :rtype: list(User)
        '''
        final_list = []
        afterMarker = 0
        while True:
            if afterMarker==0:
                response = self._http_client.make_request(
                    self._endpoint['list_initial'],
                    status = status
                )
            else:
                response = self._http_client.make_request(
                    self._endpoint['list_next'],
                    status = status,
                    after = afterMarker
                )
            for item in response['data']:
                final_list.append(as_dict(item))
            if response['nextMarker'] is None:
                break
            else:
                afterMarker = response['nextMarker']
                continue
        return [User(item, self._http_client) for item in final_list]

    def find(self, user_email):
        '''
        Find User in list objects.

        :returns: User object
        :rtype: User
        '''
        for item in self.list('ACTIVE'):
            if item._email == user_email:
                return item
        for item in self.list('DEACTIVATED'):
            if item._email == user_email:
                return item
        for item in self.list('PENDING'):
            if item._email == user_email:
                return item
        return None

    def invite_user(self, data):
        '''
        send a user invite

        :param: user email and optional group info

        :returns: True if successful
        :rtype: Boolean
        '''
        response = self._http_client.make_request(
            self._endpoint['invite_user'],
            body=data
        )
        return True

    def delete(self, user_id):
        '''
        delete a pending user

        :param: user id

        :returns: True if successful
        :rtype: Boolean
        '''
        response = self._http_client.make_request(
            self._endpoint['delete_invite'],
            userId = user_id
        )
        return response

    def update_user(self, user_id, data):
        '''
        update user data

        :param: user email and optional group info

        :returns: User object
        :rtype: User
        '''
        response = self._http_client.make_request(
            self._endpoint['update_user'],
            userId = user_id,
            body=as_dict(data)
        )
        return User(response)

    def update_user_group(self, user_id, data):
        '''
        update user data

        :param: user email and group info

        :returns: User object
        :rtype: User
        '''
        response = self._http_client.make_request(
            self._endpoint['update_user_group'],
            userId = user_id,
            body=data
        )
        return User(response)

