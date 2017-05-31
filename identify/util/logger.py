import logging
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s: %(message)s'
))

LOGGER = colorlog.getLogger('IDENTIFY')
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)
