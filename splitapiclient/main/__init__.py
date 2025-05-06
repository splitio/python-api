from splitapiclient.main.sync_apiclient import SyncApiClient
from splitapiclient.main.harness_apiclient import HarnessApiClient


def get_client(config):
    '''
    Entry point for the Split API client
    
    :param config: Dictionary containing client configuration options
        For standard mode:
            - 'apikey': Split API key for authentication
            - 'base_url': (optional) Base URL for the Split API
            - 'base_url_v3': (optional) Base URL for the Split API v3
            - 'async': (optional) Whether to use async client (not yet implemented)
        
        For harness mode:
            - 'harness_mode': Set to True to use harness mode
            - 'harness_token': Harness authentication token for x-api-key header
            - 'account_identifier': (optional) Account identifier for Harness operations
            - 'base_url': (optional) Base URL for the Harness API
    '''
    _async = config.get('async', False)
    if _async:
        raise Exception('Async client not yet implemented')
    
    # Check if harness mode is enabled
    if config.get('harness_mode', False):
        return HarnessApiClient(config)

    return SyncApiClient(config)
