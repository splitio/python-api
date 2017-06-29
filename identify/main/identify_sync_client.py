from __future__ import absolute_import, division, print_function, \
    unicode_literals
from identify.main.identify_client import BaseIdentifyClient
from identify.http_clients.sync_client import SyncHttpClient
from identify.util.exceptions import InsufficientConfigArgumentsException
from identify.microclients import TrafficTypeMicroClient
from identify.microclients import EnvironmentMicroClient
from identify.microclients import IdentityMicroClient
from identify.microclients import AttributeMicroClient


class SyncIdentifyClient(BaseIdentifyClient):
    '''
    Synchronous Identify API client
    '''

    def __init__(self, config):
        '''
        Class constructor.

        :param config: Dictionary containing optiones required to instantiate
            the API client. Shoud have AT LEAST the following keys:
                - 'base_url': Base url where the API is hosted
                - 'apikey': APIKey used to authenticate the user.
        '''
        if 'base_url' in config and 'apikey' in config:
            self._base_url = config['base_url']
            self._apikey = config['apikey']
        else:
            missing = [i not in config for i in ['base_url', 'apikey']]
            raise InsufficientConfigArgumentsException(
                'The following keys must be present in the config dict: %s'
                % ','.join(missing)
            )

        http_client = SyncHttpClient(self._base_url, self._apikey)

        self._traffic_type_client = TrafficTypeMicroClient(http_client)
        self._environment_client = EnvironmentMicroClient(http_client)
        self._attribute_client = AttributeMicroClient(http_client)
        self._identity_client = IdentityMicroClient(http_client)

    @property
    def traffic_type(self):
        return self._traffic_type_client

    @property
    def environment(self):
        return self._environment_client

    @property
    def attribute(self):
        return self._attribute_client

    @property
    def identity(self):
        return self._identity_client
