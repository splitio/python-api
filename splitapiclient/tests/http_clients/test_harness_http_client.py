from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.http_clients.harness_client import HarnessHttpClient
from splitapiclient.util.exceptions import HTTPUnauthorizedError, \
    HTTPNotFoundError, HTTPIncorrectParametersError, HTTPResponseError


class FakeResponse:
    '''
    Simple class to mock returned Response objects from the requests module.
    '''
    def __init__(self, status, text):
        self.status_code = status
        self.text = text


class TestHarnessHttpClient:
    '''
    Tests for the HarnessHttpClient class error handling
    '''

    def test_handle_invalid_response(self):
        '''
        Test that error messages include status codes and response object is passed
        '''
        c1 = HarnessHttpClient('https://app.harness.io/', 'fake_harness_token')
        
        # Test 401 Unauthorized
        with pytest.raises(HTTPUnauthorizedError) as exc_info:
            c1._handle_invalid_response(FakeResponse(401, 'Unauthorized'))
        assert 'HTTP 401' in str(exc_info.value)
        assert 'Unauthorized' in str(exc_info.value)
        assert exc_info.value._error is not None
        assert exc_info.value._error.status_code == 401
        
        # Test 400 Bad Request
        with pytest.raises(HTTPIncorrectParametersError) as exc_info:
            c1._handle_invalid_response(FakeResponse(400, 'Bad request'))
        assert 'HTTP 400' in str(exc_info.value)
        assert 'Bad request' in str(exc_info.value)
        assert exc_info.value._error.status_code == 400
        
        # Test 404 Not Found
        with pytest.raises(HTTPNotFoundError) as exc_info:
            c1._handle_invalid_response(FakeResponse(404, 'Not found'))
        assert 'HTTP 404' in str(exc_info.value)
        assert 'Not found' in str(exc_info.value)
        assert exc_info.value._error.status_code == 404
        
        # Test generic error (500 Internal Server Error)
        with pytest.raises(HTTPResponseError) as exc_info:
            c1._handle_invalid_response(FakeResponse(500, 'Internal server error'))
        assert 'HTTP 500' in str(exc_info.value)
        assert 'Internal server error' in str(exc_info.value)
        assert exc_info.value._error.status_code == 500
        
        # Test another generic error (403 Forbidden)
        with pytest.raises(HTTPResponseError) as exc_info:
            c1._handle_invalid_response(FakeResponse(403, '{"error": "Forbidden"}'))
        assert 'HTTP 403' in str(exc_info.value)
        assert 'Forbidden' in str(exc_info.value)
        assert exc_info.value._error.status_code == 403
        
        # Test JSON error response
        with pytest.raises(HTTPResponseError) as exc_info:
            c1._handle_invalid_response(FakeResponse(503, '{"message": "Service temporarily unavailable", "code": "SERVICE_UNAVAILABLE"}'))
        assert 'HTTP 503' in str(exc_info.value)
        assert 'Service temporarily unavailable' in str(exc_info.value)
        assert exc_info.value._error.status_code == 503

    def test_is_harness_endpoint(self):
        '''
        Test that Harness endpoints are correctly identified
        '''
        harness_client = HarnessHttpClient('https://app.harness.io/', 'token')
        split_client = HarnessHttpClient('https://api.split.io/internal/api/v2', 'token')
        
        # Harness endpoint should return True
        assert harness_client._is_harness_endpoint({}) == True
        
        # Split endpoint should return False
        assert split_client._is_harness_endpoint({}) == False

    def test_deprecated_endpoint_detection(self):
        '''
        Test that deprecated endpoints are correctly identified
        '''
        client = HarnessHttpClient('https://app.harness.io/', 'token')
        
        # Test workspace POST (deprecated)
        workspace_endpoint = {
            'url_template': 'workspaces/create',
            'method': 'POST'
        }
        assert client._is_deprecated_endpoint(workspace_endpoint) == True
        
        # Test workspace GET (not deprecated)
        workspace_get_endpoint = {
            'url_template': 'workspaces/list',
            'method': 'GET'
        }
        assert client._is_deprecated_endpoint(workspace_get_endpoint) == False
        
        # Test users endpoint (all methods deprecated)
        users_endpoint = {
            'url_template': 'users/123',
            'method': 'GET'
        }
        assert client._is_deprecated_endpoint(users_endpoint) == True
        
        # Test groups endpoint (all methods deprecated)
        groups_endpoint = {
            'url_template': 'groups/456',
            'method': 'POST'
        }
        assert client._is_deprecated_endpoint(groups_endpoint) == True
        
        # Test restrictions endpoint (all methods deprecated)
        restrictions_endpoint = {
            'url_template': 'restrictions/789',
            'method': 'DELETE'
        }
        assert client._is_deprecated_endpoint(restrictions_endpoint) == True
        
        # Test apiKeys with admin type (deprecated)
        apikeys_endpoint = {
            'url_template': 'apiKeys/create',
            'method': 'POST'
        }
        body_admin = {'apiKeyType': 'admin'}
        assert client._is_deprecated_endpoint(apikeys_endpoint, body_admin) == True
        
        # Test apiKeys with non-admin type (not deprecated)
        body_non_admin = {'apiKeyType': 'user'}
        assert client._is_deprecated_endpoint(apikeys_endpoint, body_non_admin) == False
        
        # Test non-deprecated endpoint
        splits_endpoint = {
            'url_template': 'splits/ws/123',
            'method': 'GET'
        }
        assert client._is_deprecated_endpoint(splits_endpoint) == False

