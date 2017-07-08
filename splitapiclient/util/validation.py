from __future__ import absolute_import, division, print_function, \
    unicode_literals
import six
from splitapiclient.util.logger import LOGGER

_validators = {
    'string': lambda value: isinstance(value, six.string_types),
    'integer': lambda value: isinstance(value, six.integer_types),
    'object': lambda value: isinstance(value, dict),
    'list': lambda value: isinstance(value, list)
}


def is_correct_type(value, schema_type):
    '''
    '''
    validator = _validators.get(schema_type.lower())
    if validator is not None:
        return validator(value)
    else:
        LOGGER.warning(
            'No validator for type {t}. Returning False by default'
            .format(t=schema_type)
        )
        return False
