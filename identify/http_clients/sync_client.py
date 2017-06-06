import json
from functools import partial
import requests
from identify.http_clients import base_client
from identify.util.logger import LOGGER
from identify.util.exceptions import HTTPResponseError, HTTPNotFoundError, \
    HTTPIncorrectParametersError, HTTPUnauthorizedError


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
        TODO
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
            raise HTTPResponseError

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
        try:
            response = method(url, headers=headers)
        except Exception as e:
            return self._connection_error(e)
        finally:
            LOGGER.debug('RESPONSE: ' + response.text)

        if not response.status_code == 200:
            LOGGER.warning('RESPONSE CODE: %s' % response.status_code)
            self._handle_invalid_response(response)

        if endpoint.get('response', False):
            return json.loads(response.text)
