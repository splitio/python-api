from __future__ import absolute_import, division, print_function, \
    unicode_literals
import json
import time
from functools import partial
import requests
from splitapiclient.http_clients import base_client
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.exceptions import HTTPResponseError, \
    HTTPNotFoundError, HTTPIncorrectParametersError, HTTPUnauthorizedError, \
    SplitBackendUnreachableError, HarnessDeprecatedEndpointError, MissingParametersException


class HarnessHttpClient(base_client.BaseHttpClient):
    '''
    Harness mode HTTP client.
    This client will block on every http request until a response is received.
    It will also enforce restrictions on deprecated endpoints in harness mode.
    '''

    # List of deprecated endpoints in harness mode
    DEPRECATED_ENDPOINTS = {
        'workspaces': ['POST', 'PATCH', 'DELETE', 'PUT'],
        'apiKeys': {
            'admin': ['POST']
        },
        'users': ['GET', 'POST', 'PATCH', 'DELETE', 'PUT'],
        'groups': ['GET', 'POST', 'PATCH', 'DELETE', 'PUT'],
        'restrictions': ['GET', 'POST', 'PATCH', 'DELETE', 'PUT']
    }

    def __init__(self, baseurl, auth_token):
        '''
        Class constructor. Stores basic connection information.

        :param baseurl: string. Harness host and base url.
        :param auth_token: string. Harness authentication token needed to make API calls.
        '''
        # Initialize with empty base_args - we'll handle auth differently in harness mode
        self.config = {
            'base_url': baseurl,
            'base_args': {}
        }
        # Store the auth token
        self._auth_token = auth_token

    def setup_method(self, method, body=None):
        '''
        Wraps 'requests' module functions by partially applying the body
        parameter when needed to provide a standardized interface.

        :param method: string. GET | POST | PATCH | PUT | DELETE
        :param body: object/list. Body for methods that use it.

        :rtype: function
        '''
        methods = {
            'GET': requests.get,
            'POST': partial(requests.post, json=body),
            'PUT': partial(requests.put, json=body),
            'PATCH': partial(requests.patch, json=body),
            'DELETE': requests.delete
        }

        return methods[method]

    def _is_deprecated_endpoint(self, endpoint, body=None):
        '''
        Checks if the endpoint is deprecated in harness mode.

        :param endpoint: dict. Endpoint description.
        :param body: dict/list. Request body.

        :return: bool. True if the endpoint is deprecated, False otherwise.
        '''
        url_template = endpoint['url_template']
        method = endpoint['method']
        
        # Check for workspaces endpoint
        if url_template.startswith('workspaces') and method in self.DEPRECATED_ENDPOINTS['workspaces']:
            return True
            
        # Check for apiKeys endpoint with admin type
        if url_template.startswith('apiKeys') and method in self.DEPRECATED_ENDPOINTS['apiKeys']['admin']:
            if body and body.get('apiKeyType') == 'admin':
                return True
                
        # Check for users endpoint
        if url_template.startswith('users'):
            return True
            
        # Check for groups endpoint
        if url_template.startswith('groups'):
            return True
            
        # Check for restrictions endpoint
        if url_template.startswith('restrictions'):
            return True
            
        return False

    def _is_harness_endpoint(self, endpoint):
        '''
        Determines if the endpoint is a Harness-specific endpoint based on the base URL.
        
        :param endpoint: dict. Endpoint description.
        :return: bool. True if the endpoint is a Harness endpoint, False otherwise.
        '''
        # In the harness client, we can determine if it's a Harness endpoint by checking the base URL
        # Split API base URLs are typically api.split.io
        # Harness API base URLs are typically app.harness.io
        return 'app.harness.io' in self.config['base_url']

    def _handle_invalid_response(self, response):
        '''
        Handle responses that are not okay and throw an appropriate exception.
        If the code doesn't match the known ones, a generic HTTPResponseError
        is thrown

        :param response: requests' module response object
        '''
        status_codes_exceptions = {
            404: HTTPNotFoundError,
            401: HTTPUnauthorizedError,
            400: HTTPIncorrectParametersError,
        }

        exc = status_codes_exceptions.get(response.status_code)
        if exc:
            raise exc(response.text)
        else:
            raise HTTPResponseError(response.text)

    def _handle_connection_error(self, e):
        '''
        Handle error when attempting to connect to split backend.
        Logs exception thrown by requests module, and raises an
        SplitBackendUnreachableError error, so that it can be caught
        by using the top level SplitException
        '''
        LOGGER.debug(e)
        raise SplitBackendUnreachableError(
            'Unable to reach Harness backend'
        )
        
    @staticmethod
    def validate_params(endpoint, all_arguments):
        '''
        Override the base client validation to handle harness mode authentication.
        In harness mode, we use x-api-key instead of Authorization, so we need to
        modify the validation logic to not require the Authorization header.
        
        :param endpoint: dict. Endpoint description
        :param all_arguments: Parameter values
        
        :rtype: None
        '''
        # Get required parameters from URL template and query string
        url_params = base_client.BaseHttpClient.get_params_from_url_template(endpoint['url_template'])
        query_params = [i['name'] for i in endpoint['query_string'] if i['required']]
        
        # Add required headers, but exclude 'Authorization' since we're using 'x-api-key' in harness mode
        header_params = []
        for header in endpoint['headers']:
            if header['required'] and header['name'] != 'Authorization':
                header_params.append(header['name'])
        
        # Combine all required parameters
        required_params = url_params + header_params + query_params
        
        # Check if any required parameters are missing
        missing = [p for p in required_params if p not in all_arguments]
        
        if missing:
            raise MissingParametersException(
                'The following required parameters are missing: {missing}'
                .format(missing=', '.join(missing))
            )

    def _setup_headers(self, endpoint, params):
        '''
        Override the base client _setup_headers method to handle harness mode authentication.
        In harness mode, we need to skip 'Authorization' headers and use 'x-api-key' instead.
        
        :param endpoint: dict. Endpoint description
        :param params: dict. List of parameter values
        
        :rtype: dict.
        '''
        # Set up required headers except 'Authorization'
        headers = {}
        for header in endpoint['headers']:
            if header.get('required', False):
                # Skip 'Authorization' header in harness mode
                if header['name'] == 'Authorization':
                    continue
                if header['name'] in params:
                    headers[header['name']] = base_client.BaseHttpClient._process_single_header(
                        header, params[header['name']]
                    )
        
        # Add optional headers
        headers.update({
            header['name']: base_client.BaseHttpClient._process_single_header(
                header, params[header['name']]
            )
            for header in endpoint['headers']
            if (not header.get('required', False)) and header['name'] in params
        })
        
        # Add x-api-key header
        if 'x-api-key' in params:
            headers['x-api-key'] = params['x-api-key']
        
        return headers

    def make_request(self, endpoint, body=None, **kwargs):
        '''
        This method delegates building of headers, url and querystring (!)
        to separate functions and then calls the appropriate method of the
        requests module with the required arguments. Logs plenty of debug data,
        and raises an exception if the response code is not 200.

        :param endpoint: dict. Endpoint description (url, headers, qs, etc).
        :param body: list/dict. Body used for POST/PATCH/PUT requests
        :param kwargs: dict. Extra arguments (values).

        :rtype: dict/list/None
        '''
        # Check if the endpoint is deprecated in harness mode
        if self._is_deprecated_endpoint(endpoint, body):
            raise HarnessDeprecatedEndpointError(
                f"Endpoint {endpoint['url_template']} with method {endpoint['method']} is deprecated in harness mode"
            )
            
        # In harness mode, use x-api-key header for all endpoints
        kwargs['x-api-key'] = self._auth_token
            
        kwargs.update(self.config['base_args'])
        self.validate_params(endpoint, kwargs)

        url = self._setup_url(endpoint, kwargs)
        headers = self._setup_headers(endpoint, kwargs)
        method_name = endpoint['method']
        method = self.setup_method(method_name, body)

        LOGGER.debug('{method} {url}'.format(method=method_name, url=url))
        LOGGER.debug('HEADERS: {headers}'.format(headers=headers))
        if body:
            LOGGER.debug('BODY: ' + json.dumps(body))

        # Make the actual HTTP call!
        while True:
            try:
                response = method(url, headers=headers)
                LOGGER.debug('RESPONSE: ' + response.text)
            except Exception as e:
                return self._handle_connection_error(e)
            if response.status_code==429:
                LOGGER.warning('RESPONSE CODE: %s, retrying in 5 seconds' % response.status_code)
                time.sleep(5)
                continue
            else:
                break
            
        if not (response.status_code == 200 or response.status_code == 204 or response.status_code == 201):
            LOGGER.warning('RESPONSE CODE: %s' % response.status_code)
            self._handle_invalid_response(response)

        if endpoint.get('response', False):
            if response.status_code != 204:
                return json.loads(response.text)
