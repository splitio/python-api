from identify.main.identify_sync_client import SyncIdentifyClient
from identify.util import logger


def get_client(config):
    '''
    Entry point for the Identify API client
    '''
    _async = config.get('async', False)
    if _async: raise Exception('Async client not yet implemented')

    if 'log_level' in config:
        logger.set_level(config['log_level'])

    return SyncIdentifyClient(config)
