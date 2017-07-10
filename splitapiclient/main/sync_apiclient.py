from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.main.apiclient import BaseApiClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.util.exceptions import InsufficientConfigArgumentsException
from splitapiclient.microclients import TrafficTypeMicroClient
from splitapiclient.microclients import EnvironmentMicroClient
from splitapiclient.microclients import IdentityMicroClient
from splitapiclient.microclients import AttributeMicroClient


class SyncApiClient(BaseApiClient):
    '''
    Synchronous Split API client
    '''

    BASE_PROD_URL = 'https://api.split.io/internal/api/v1'

    def __init__(self, config):
        '''
        Class constructor.

        :param config: Dictionary containing optiones required to instantiate
            the API client. Shoud have AT LEAST the following keys:
                - 'base_url': Base url where the API is hosted
                - 'apikey': APIKey used to authenticate the user.
        '''
        if 'base_url' in config:
            self._base_url = config['base_url']
        else:
            self._base_url = self.BASE_PROD_URL

        missing = [i for i in ['apikey'] if i not in config]
        if missing:
            raise InsufficientConfigArgumentsException(
                'The following keys must be present in the config dict: %s'
                % ','.join(missing)
            )

        self._apikey = config['apikey']
        http_client = SyncHttpClient(self._base_url, self._apikey)

        self._traffic_type_client = TrafficTypeMicroClient(http_client)
        self._environment_client = EnvironmentMicroClient(http_client)
        self._attribute_client = AttributeMicroClient(http_client)
        self._identity_client = IdentityMicroClient(http_client)

    @property
    def traffic_types(self):
        return self._traffic_type_client

    @property
    def environments(self):
        return self._environment_client

    @property
    def attributes(self):
        return self._attribute_client

    @property
    def identities(self):
        return self._identity_client
