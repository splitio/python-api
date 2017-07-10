from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.util.exceptions import MissingParametersException


class TestBaseHTTPClient:
    '''
    '''
    def test_get_params_from_url_template(self):
        '''
        '''
        cases = [{
            'url': 'http://localhost/a/b/c',
            'params': []
        }, {
            'url': 'http://host/{a}/{b}/c',
            'params': ['a', 'b']
        }, {
            'url': '',
            'params': []
        }, {
            'url': 'http://host/{a}/{b}/{a}',
            'params': ['a', 'b']
        }]

        for case in cases:
            assert (
                set(BaseHttpClient.get_params_from_url_template(case['url'])) ==
                set(case['params'])
            )

    def test_process_single_header(self):
        '''
        '''
        cases = [{
            'header': {},
            'value': 'the_value',
            'output': 'the_value'
        }, {
            'header': {'some_other_property': 'some_value'},
            'value': 'the_value',
            'output': 'the_value'
        }, {
            'header': {'template': '{value} and some_value'},
            'value': 'the_value',
            'output': 'the_value and some_value'
        }]
        for case in cases:
            assert (
                BaseHttpClient._process_single_header(case['header'], case['value']) ==
                case['output']
            )

    def test_setup_headers(self, mocker):
        '''
        '''
        cases = [{
            'endpoint': {'headers': [{'name': 'a', 'required': True}]},
            'params': {'a': 'test'},
            'expected': ({'name': 'a', 'required': True}, 'test')
        }]
        with mocker.patch('splitapiclient.http_clients.base_client.BaseHttpClient._process_single_header'):
            for case in cases:
                BaseHttpClient._setup_headers(case['endpoint'], case['params'])
                BaseHttpClient._process_single_header.assert_called_once_with(
                    *case['expected']
                )

    def test_setup_url(self):
        '''
        '''
        class FakeClient(BaseHttpClient):
            def make_request(self):
                pass

        fc1 = FakeClient('http://a/b.com', 'fake_api_key')
        cases = [{
            'endpoint': {'url_template': 'nothing'},
            'params': {},
            'expected': 'http://a/b.com/nothing'
        }, {
            'endpoint': {'url_template': 'something_{a}'},
            'params': {'a': 'in_the_way'},
            'expected': 'http://a/b.com/something_in_the_way'
        }]

        for case in cases:
            assert (fc1._setup_url(case['endpoint'], case['params']) ==
                    case['expected'])

    def test_validate_params(self):
        '''
        '''
        cases = [{
            'endpoint': {
                'headers': [{'name': 'header1', 'required': False}],
                'query_string': [],
                'url_template': 'some'
            },
            'raises': False
        }, {
            'endpoint': {
                'headers': [{'name': 'header1', 'required': True}],
                'query_string': [],
                'url_template': 'some'
            },
            'raises': True
        }, {
            'endpoint': {
                'headers': [],
                'query_string': [{'name': 'some_prop', 'required': True}],
                'url_template': 'some'
            },
            'raises': True
        }, {
            'endpoint': {
                'headers': [],
                'query_string': [],
                'url_template': 'some/{val}'
            },
            'raises': True
        }]

        for case in cases:
            if case['raises']:
                with pytest.raises(MissingParametersException):
                    BaseHttpClient.validate_params(case['endpoint'], {})
