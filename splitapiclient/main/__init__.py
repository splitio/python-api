from splitapiclient.main.sync_apiclient import SyncApiClient


def get_client(config):
    '''
    Entry point for the Split API client
    '''
    _async = config.get('async', False)
    if _async:
        raise Exception('Async client not yet implemented')

    return SyncApiClient(config)
