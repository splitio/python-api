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
    SplitBackendUnreachableError


class SyncHttpClient(base_client.BaseHttpClient):
    '''
    Synchronous API client.
    This client will block on every http request until a response is received.
    '''

    def setup_method(self, method, body=None):
        '''
        Wraps 'requests' module functions by partially applying the body
        parameter when needed to provide a standarized interface.

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
            raise exc()
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
            'Unable to reach Split backend'
        )

    def make_request(self, endpoint, body=None, **kwargs):
        '''
        This method delegates bulding of headers, url and querystring (!)
        to separate functions and then calls the appropriate method of the
        requests module with the required arguments. Logs plenty of debug data,
        and raises an exception if the response code is not 200.

        :param endpoint: dict. Endpoint description (url, headers, qs, etc).
        :param body: list/dict. Body used for POST/PATCH/PUT requests
        :param kwargs: dict. Extra arguments (values).

        :rtype: dict/list/None
        '''
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
            
        if not (response.status_code == 200 or response.status_code == 204):
            LOGGER.warning('RESPONSE CODE: %s' % response.status_code)
            self._handle_invalid_response(response)

        if endpoint.get('response', False):
            if response.status_code != 204:
                return json.loads(response.text)
