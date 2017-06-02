from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from identify.resources.base_resource import BaseResource
from identify.util.exceptions import HTTPResponseError, EndpointNotImplemented


class TestBaseResource:
    '''
    Tests for the BaseResource class' methods
    '''

    def test_constructor(self):
        '''
        '''
        class SampleResource(BaseResource):
            pass

        with pytest.raises(TypeError):
            a = SampleResource('', '')

        class SampleResource2(BaseResource):
            _endpoint = {}
            _schema = {}
            def _build_single_from_collection_response(self, c, r): pass

        b = SampleResource2('', '')
        assert isinstance(b, BaseResource)

    def test_process_all_response(self, mocker):
        '''
        '''
        items = ['item1', 'item2', 'item3', 'item4', 'item5']
        with mocker.patch('identify.resources.base_resource.BaseResource'
                          '._build_single_from_collection_response'):
            BaseResource._process_all_response('client', items)

            calls = [mocker.call('client', item) for item in items]
            (BaseResource._build_single_from_collection_response
             .assert_has_calls(calls))

    def test_retrieve_all(self, mocker):
        '''
        '''
        successful_client = mocker.Mock()
        successful_client.make_request.return_value = ['item1', 'item2']

        failed_client = mocker.Mock()
        failed_client.make_request.side_effect=HTTPResponseError()

        with mocker.patch('identify.resources.base_resource.BaseResource'
                          '._process_all_response'):

            class HasAllItemsEndpoint(BaseResource):
                _endpoint = {'all_items': {"asd": 1}}
                _schema = {}
                def _build_single_from_collection_response(self, c, r): pass

            class DoesntHaveAllItemsEndpoint(BaseResource):
                _endpoint = {}
                _schema = {}
                def _build_single_from_collection_response(self, c, r): pass

            cases = [{
                'resource': HasAllItemsEndpoint,
                'client': successful_client,
                'process_call_args': ['item1', 'item2']
            }, {
                'resource': DoesntHaveAllItemsEndpoint,
                'client': successful_client,
                'raises': EndpointNotImplemented
            }, {
                'resource': HasAllItemsEndpoint,
                'client': failed_client,
            }, {
                'resource': DoesntHaveAllItemsEndpoint,
                'client': failed_client,
                'raises': EndpointNotImplemented
            }]

            for case in cases:
                if 'raises' in case:
                    # Cases with no "all_items" endpoint
                    with pytest.raises(case['raises']):
                        case['resource'].retrieve_all(case['client'])
                elif 'process_call_args' in case:
                    # Successfun case
                    case['resource'].retrieve_all(case['client'])
                    (HasAllItemsEndpoint._process_all_response
                     .assert_called_once_with(
                         case['client'],
                         case['process_call_args']
                     ))
                else:
                    assert case['resource'].retrieve_all(case['client']) == []
