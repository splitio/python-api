from __future__ import absolute_import, division, print_function, \
    unicode_literals
import re


_CAPS_TO_UNDERSCORE_REGEX = re.compile('(.)([A-Z][a-z]+)')
_NUMBERS_TO_UNDERSCORE_REGEX = re.compile('([a-z0-9])([A-Z])')


def to_underscore(name):
    s1 = _CAPS_TO_UNDERSCORE_REGEX.sub(r'\1_\2', name)
    return _NUMBERS_TO_UNDERSCORE_REGEX.sub(r'\1_\2', s1).lower()


def from_underscore(name):

    if not name:
        return ''

    def camelcase_func_it():
        yield 'lower'
        while True:
            yield 'capitalize'

    c = camelcase_func_it()
    return ''.join(getattr(x, next(c))() if x else '_' for x in name.split("_"))
