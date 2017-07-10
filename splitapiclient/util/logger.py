from __future__ import absolute_import, division, print_function, \
    unicode_literals
import logging

try:
    from logging import NullHandler
except ImportError:   # Python 2.7+
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


logging.getLogger(__name__).addHandler(NullHandler())

_LOGLEVELS = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
}


LOGGER = logging.getLogger('IDENTIFY')
LOGGER.addHandler(NullHandler())
