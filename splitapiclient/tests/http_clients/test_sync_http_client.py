from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.http_clients import sync_client
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.util.exceptions import HTTPUnauthorizedError, \
    HTTPNotFoundError,  HTTPIncorrectParametersError


class FakeResponse:
    '''
    Simple class to mock returned Response objects from the requests module.
    '''
    def __init__(self, status, text):
        self.status_code = status
        self.text = text


class TestSyncHttpClient:
    '''
    Tests for the SyncHttpClient class
    '''

    def test_setup_method(self, mocker):
        '''
        '''
        c1 = SyncHttpClient('http://a.b.com', 'fake_api_key')

        mocker.patch('splitapiclient.http_clients.sync_client.requests.get')
        mocker.patch('splitapiclient.http_clients.sync_client.requests.post')
        mocker.patch('splitapiclient.http_clients.sync_client.requests.put')
        mocker.patch('splitapiclient.http_clients.sync_client.requests.patch')
        mocker.patch('splitapiclient.http_clients.sync_client.requests.delete')

        c1.setup_method('GET', None)()
        sync_client.requests.get.assert_called_once_with()

        sync_client.requests.get.reset_mock()
        c1.setup_method('GET', {'something': 'a'})()
        sync_client.requests.get.assert_called_once_with()

        c1.setup_method('POST', None)()
        sync_client.requests.post.assert_called_once_with(json=None)

        sync_client.requests.post.reset_mock()
        c1.setup_method('POST', {'something': 'a'})()
        sync_client.requests.post.assert_called_once_with(json={'something': 'a'})

        c1.setup_method('PUT', None)()
        sync_client.requests.put.assert_called_once_with(json=None)

        sync_client.requests.put.reset_mock()
        c1.setup_method('PUT', {'something': 'a'})()
        sync_client.requests.put.assert_called_once_with(json={'something': 'a'})

        c1.setup_method('PATCH', None)()
        sync_client.requests.patch.assert_called_once_with(json=None)

        sync_client.requests.patch.reset_mock()
        c1.setup_method('PATCH', {'something': 'a'})()
        sync_client.requests.patch.assert_called_once_with(json={'something': 'a'})

        c1.setup_method('DELETE', {'something': 'a'})()
        sync_client.requests.delete.assert_called_once_with()

        sync_client.requests.delete.reset_mock()
        c1.setup_method('DELETE', {'something': 'a'})()
        sync_client.requests.delete.assert_called_once_with()

    def test_handle_invalid_response(self):
        '''
        '''
        c1 = SyncHttpClient('http://a.b.com', 'fake_api_key')
        with pytest.raises(HTTPUnauthorizedError):
            c1._handle_invalid_response(FakeResponse(401, ''))
        with pytest.raises(HTTPIncorrectParametersError):
            c1._handle_invalid_response(FakeResponse(400, ''))
        with pytest.raises(HTTPUnauthorizedError):
            c1._handle_invalid_response(FakeResponse(401, ''))

    def test_make_request(self, mocker):
        '''
        '''
        c1 = SyncHttpClient('http://a.b.com', 'fake_api_key')

        mocker.patch('splitapiclient.http_clients.sync_client.requests.get')
        mocker.patch('splitapiclient.http_clients.sync_client.requests.post')
        mocker.patch('splitapiclient.http_clients.sync_client.requests.put')
        mocker.patch('splitapiclient.http_clients.sync_client.requests.patch')
        mocker.patch('splitapiclient.http_clients.sync_client.requests.delete')

        cases = [{  # Successful GET
            'endpoint': {
                'method': 'GET',
                'url_template': 'abc',
                'headers': [],
                'query_string': '',
                'response': True
            },
            'body': None,
            'params': {},
            'mock': sync_client.requests.get,
            'response': FakeResponse(200, '{"valid": "json"}')
        }, {  # Unauthorized GET
            'endpoint': {
                'method': 'GET',
                'url_template': 'abc',
                'headers': [],
                'query_string': '',
                'response': True
            },
            'body': None,
            'params': {},
            'mock': sync_client.requests.get,
            'response': FakeResponse(401, '{"valid": "json"}'),
            'raises': HTTPUnauthorizedError,
        }, {  # Not Found GET
            'endpoint': {
                'method': 'GET',
                'url_template': 'abc',
                'headers': [],
                'query_string': '',
                'response': True
            },
            'body': None,
            'params': {},
            'mock': sync_client.requests.get,
            'response': FakeResponse(404, '{"valid": "json"}'),
            'raises': HTTPNotFoundError,
        }, {  # Incorrect parameters
            'endpoint': {
                'method': 'GET',
                'url_template': 'abc',
                'headers': [],
                'query_string': '',
                'response': True
            },
            'body': None,
            'params': {},
            'mock': sync_client.requests.get,
            'response': FakeResponse(400, '{"valid": "json"}'),
            'raises': HTTPIncorrectParametersError,
        }, {  # Successful POST
            'endpoint': {
                'method': 'POST',
                'url_template': 'abc',
                'headers': [],
                'query_string': '',
                'response': True
            },
            'body': '{"some": "valid body"}',
            'params': {},
            'mock': sync_client.requests.post,
            'response': FakeResponse(200, '{"valid": "json"}')
        }, {  # Successful PATCH
            'endpoint': {
                'method': 'PATCH',
                'url_template': 'abc',
                'headers': [],
                'query_string': '',
                'response': True
            },
            'body': '{"some": "valid body"}',
            'params': {},
            'mock': sync_client.requests.patch,
            'response': FakeResponse(200, '{"valid": "json"}')
        }, {  # Successful PUT
            'endpoint': {
                'method': 'PUT',
                'url_template': 'abc',
                'headers': [],
                'query_string': '',
                'response': True
            },
            'body': '{"some": "valid body"}',
            'params': {},
            'mock': sync_client.requests.put,
            'response': FakeResponse(200, '{"valid": "json"}')
        }, {  # Successful DELETE
            'endpoint': {
                'method': 'DELETE',
                'url_template': 'abc',
                'headers': [],
                'query_string': '',
                'response': True
            },
            'body': '',
            'params': {},
            'mock': sync_client.requests.delete,
            'response': FakeResponse(200, '{"valid": "json"}')
        }]

        for case in cases:
            case['mock'].reset_mock()
            case['mock'].return_value = case['response']
            exc = case.get('raises', None)
            named_args = {'headers': {}}
            if case.get('body'): named_args['json'] = case['body']
            if exc:
                with pytest.raises(exc):
                    c1.make_request(
                        case['endpoint'],  case['body'], **case['params']
                    )
            else:
                c1.make_request(
                    case['endpoint'],  case['body'], **case['params']
                )
                case['mock'].assert_called_once_with(
                    '%s/%s' % (c1.config['base_url'], case['endpoint']['url_template']),
                    **named_args
                )
