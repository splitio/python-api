import logging
import colorlog

_LOGLEVELS = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
}


handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s: %(message)s'
))

LOGGER = colorlog.getLogger('IDENTIFY')
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)


def set_level(strlevel):
    '''
    '''
    lvl = _LOGLEVELS.get(strlevel.upper())
    if not lvl:
        raise Exception('Invalid Log Level %s' % strlevel)
    LOGGER.setLevel(lvl)
