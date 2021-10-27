from __future__ import absolute_import, division, print_function, \
    unicode_literals
import abc
import re
import six
from splitapiclient.util.exceptions import MissingParametersException


class BaseHttpClient(six.with_metaclass(abc.ABCMeta)):
    '''
    Abstrac class providing an interface and generic methods of the HTTP client
    responsible for interacting with the Split APIs
    '''

    def __init__(self, baseurl, auth_token):
        '''
        Class constructor. Sotores basic connection information.

        :param baseurl: string. Split host and base url.
        :param auth_token: string. Authentication token needed to make API
            calls.
        '''
        self.config = {
            'base_url': baseurl,
            'base_args': {
                'Authorization': auth_token
            }
        }

    @abc.abstractmethod
    def make_request(self, method, body=None, **kwargs):
        '''
        Method responsible for executing an actual requesting, retrievieng an
        appropiarte response and raising an exception if the HTTP call fails.

        :param endpoint: dict. Endpoint description (method, url, etc)
        :param body: dict/list. POST/PUT/PATCH request body (optional)
        :param kwargs: dict. Extra parameters required for headers, querystring,
            url template paramters, etc.

        :rtype: dict/list/None
        '''
        pass

    @staticmethod
    def get_params_from_url_template(url):
        '''
        Retuns a list of templated variables that must be replaced when
        instantiating the url template.

        :param url: url template

        :rtype: list.
        '''
        regex = '{([\w-]+)}*'
        url_params = re.findall(regex, url)
        return list(set(url_params)) if url_params else []

    @staticmethod
    def _process_single_header(header, value):
        '''
        Checks if the header's value is a templated string. If that is the case,
        the template is instantiated with the correct value. Otherwise the
        single value is returned.

        :param header: dict. Header description from endpoint.
        :param value: string. Header value

        rtype: string.
        '''
        template = header.get('template')
        if template:
            return template.format(value=value)
        else:
            return value

    @staticmethod
    def _setup_headers(endpoint, params):
        '''
        Returns a dictionary with header_name: value format.
        Mandatory headers are always added and an exception will be thrown
        if the value is not available.
        Optional headers are only added if the value is available in params.

        :param endpoint: dict. Endpoint description
        :param params: dict. List of parameter values

        :rtype: dict.
        '''
        headers = {
            header['name']: BaseHttpClient._process_single_header(
                header, params[header['name']]
            )
            for header in endpoint['headers']
            if header.get('required', False)
        }

        # add optional headers
        headers.update({
            header['name']: BaseHttpClient._process_single_header(
                header, params[header['name']]
            )
            for header in endpoint['headers']
            if (not header.get('required', False)) and header['name'] in params
        })

        return headers

    def _setup_url(self, endpoint, params):
        '''
        Instantiates the url template with values supplied in params.

        :param endpoint: dict. Endpoint description.
        :param params: dict. Parameter values.

        :rtype: string.
        '''
        base_template = '{base}/{endpoint}'.format(
            base=self.config['base_url'],
            endpoint=endpoint['url_template']
        )

        params_for_url = BaseHttpClient.get_params_from_url_template(
            base_template
        )

        parameter_values = {
            param: params[param]
            for param in params
            if param in params_for_url
        }

        return base_template.format(**parameter_values)

    @staticmethod
    def validate_params(endpoint, all_arguments):
        '''
        Checks that all the required parameters are supplied. Raises an
        exception otherwise.

        :param endpoint: dict. Endpoint description
        :param all_arguments: Parameter values

        :rtype: None
        '''
        required_params = (
            BaseHttpClient.get_params_from_url_template(endpoint['url_template']) +
            [i['name'] for i in endpoint['headers'] if i['required']] +
            [i['name'] for i in endpoint['query_string'] if i['required']]
        )

        missing = [p for p in required_params if p not in all_arguments]

        if missing:
            raise MissingParametersException(
                'The following required parameters are missing: {missing}'
                .format(missing=', '.join(missing))
            )
