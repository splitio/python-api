from identify.main.identify_sync_client import SyncIdentifyClient


def get_client(config):
    '''
    Entry point for the Identify API client
    '''
    _async = config.get('async', False)
    if _async:
        raise Exception('Async client not yet implemented')

    return SyncIdentifyClient(config)
