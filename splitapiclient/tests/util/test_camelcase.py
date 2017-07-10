from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.util.camelcase import to_underscore, from_underscore


class TestCamelCaseUtils:
    '''
    Tests for the camelcase module utilities
    '''

    def test_to_underscore(self):
        '''
        Test that camelcase names are correctly converted to underscores.
        '''
        cases = [{
            'in': 'camelCase',
            'out': 'camel_case',
        }, {
            'in': 'camelcase',
            'out': 'camelcase',
        }, {
            'in': 'CamelCase',
            'out': 'camel_case',
        }, {
            'in': 'camelCCase',
            'out': 'camel_c_case',
        }, {
            'in': '',
            'out': '',
        }, {
            'in': 'camel3Case',
            'out': 'camel3_case',
        }, {
            'in': 'camelCaseMultipleWords',
            'out': 'camel_case_multiple_words',
        }, {
            'in': 'camelCase_Underscore',
            'out': 'camel_case__underscore',
        }]

        for case in cases:
            assert to_underscore(case['in']) == case['out']

    def test_from_underscore(self):
        '''
        Test that camelcase names are correctly converted to underscores.
        '''
        cases = [{
            'out': 'camelCase',
            'in': 'camel_case',
        }, {
            'out': 'camelcase',
            'in': 'camelcase',
        }, {
            'out': 'camelCase',
            'in': 'camel_case',
        }, {
            'out': 'camelCCase',
            'in': 'camel_c_case',
        }, {
            'out': '',
            'in': '',
        }, {
            'out': 'camel3Case',
            'in': 'camel3_case',
        }, {
            'out': 'camelCaseMultipleWords',
            'in': 'camel_case_multiple_words',
        }, {
            'out': 'camelCase_Underscore',
            'in': 'camel_case__underscore',
        }]

        for case in cases:
            assert from_underscore(case['in']) == case['out']
