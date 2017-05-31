import re


_CAPS_TO_UNDERSCORE_REGEX = re.compile('(.)([A-Z][a-z]+)')
_NUMBERS_TO_UNDERSCORE_REGEX = re.compile('([a-z0-9])([A-Z])')


def to_underscore(name):
    s1 = _CAPS_TO_UNDERSCORE_REGEX.sub(r'\1_\2', name)
    return _NUMBERS_TO_UNDERSCORE_REGEX.sub(r'\1_\2', s1).lower()


def from_underscore(name):
    def camelcase():
        yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()
    return ''.join(c.next()(x) if x else '_' for x in name.split("_"))
