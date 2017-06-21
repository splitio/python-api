from __future__ import absolute_import, division, print_function, \
    unicode_literals
from identify.main.identify_client import BaseIdentifyClient
from identify.http_clients.sync_client import SyncHttpClient
from identify.resources.traffic_type import TrafficType
from identify.resources.environment import Environment
from identify.resources.attribute import Attribute
from identify.resources.identity import Identity
from identify.util.exceptions import InsufficientConfigArgumentsException


class TrafficTypeMicroClient:
    '''
    '''

    def __init__(self, http_client):
        '''
        '''
        self._http_client = http_client

    def get_all(self):
        '''
        Returns a list of TrafficType objects.
        '''
        return TrafficType.retrieve_all(self._http_client)


class EnvironmentMicroClient:
    '''
    '''

    def __init__(self, http_client):
        '''
        '''
        self._http_client = http_client

    def get_all(self):
        '''
        Returns a list of environments.
        '''
        return Environment.retrieve_all(self._http_client)


class AttributeMicroClient:
    '''
    '''

    def __init__(self, http_client):
        '''
        '''
        self._http_client = http_client

    def get_all(self, traffic_type_id):
        '''
        Returns a list of attributes for a particular traffic type.

        :param traffic_type_id: Id of the traffic type whose attributes are to
            be retrieved.
        '''
        return Attribute.retrieve_all(
            self._http_client,
            trafficTypeId=traffic_type_id
        )

    def create(self, traffic_type_id, attr_id, display_name, description,
               data_type, is_searchable):
        '''
        Creates an attribute for a specific traffic type.

        :param traffic_type_id: Id of the traffic type for which an attribute
            will be created.
        :param attr_id: string. New attribute's Id
        :param display_name: string. New attribute's display name
        :param description: string. New attribute's description
        :param data_type: string. New attribute's data type
        :param is_searchable: string.
        '''
        return Attribute.create(
            self._http_client,
            attr_id,
            traffic_type_id,
            display_name,
            description,
            data_type,
            is_searchable
        )

    def delete(self, traffic_type_id, attribute_id):
        '''
        Delete an attribute from a particular traffic type.

        :param traffic_type_id: Trafic id of the schema whose attribute
            will be removed.
        :param attribute_id: Id of the attribute to be removed.
        '''
        return Attribute.delete(
            self._http_client,
            attribute_id,
            traffic_type_id
        )


class IdentityMicroClient:
    '''
    '''

    def __init__(self, http_client):
        '''
        '''
        self._http_client = http_client

    def add_many(self, traffic_type_id, environment_id, identities,
                 organization_id=None):
        '''
        Create Identities for a specific traffic type and environment.

        :param traffic_type_id: Traffic type id
        :param environment_id: Environment where the identities will be created.
        :param identities: Identities to be added. Should be in a dict with
            the following format:
                {
                    'key1': {
                        attribute_id_1a: value_1a,
                        attribute_id_1b: value_1b,
                    },
                    'key2': {
                        attribute_id_2a: value_2a,
                        attribute_id_2b: value_2b,
                    }
                }
        '''
        return Identity.create_many(
            self._http_client,
            traffic_type_id,
            environment_id,
            identities,
            organization_id
        )

    def add(self, traffic_type_id, environment_id, key, values,
            organization_id=None):
        '''
        Create a new Identity.

        :param traffic_type_id: Traffic Type Id
        :param environment_id: Environment where the identity will be created.
        :key: Identity key
        :values: Attribute values for the identity. Should be a dict with
             the following format:
                 {
                    attribute_id1: value1,
                    attribute_id2: value2,
                 }
        '''
        return Identity.create(
            self._http_client,
            key,
            traffic_type_id,
            environment_id,
            values,
            organization_id
        )

    def update(self, traffic_type_id, environment_id, key, values,
               organization_id=None):
        '''
        Update an Identity.

        :param traffic_type_id: Traffic Type Id
        :param environment_id: Environment where the identity will be updated.
        :key: Identity key
        :values: Attribute values for the identity. Should be a dict with
             the following format:
                 {
                    attribute_id1: value1,
                    attribute_id2: value2,
                 }
        '''
        return Identity.update(
            self._http_client,
            key,
            traffic_type_id,
            environment_id,
            values,
            organization_id
        )

    def patch(self, traffic_type_id, environment_id, key, values,
              organization_id=None):
        '''
        Patch an Identity.

        :param traffic_type_id: Traffic Type Id
        :param environment_id: Environment where the identity will be patched.
        :key: Identity key
        :values: Attribute values for the identity. Should be a dict with
             the following format:
                 {
                    attribute_id1: value1,
                    attribute_id2: value2,
                 }
        '''
        return Identity.patch(
            self._http_client,
            key,
            traffic_type_id,
            environment_id,
            values,
            organization_id
        )

    def delete_attributes(self, traffic_type_id, environment_id, key):
        '''
        Delete all attributes for a specific key.

        :param traffic_type_id: Traffic Type Id,
        :param environment_id: Enviroment Id,
        :key: Key whose attributes will be deleted.
        '''
        return Identity.delete_all_attributes(
            self._http_client,
            traffic_type_id,
            environment_id,
            key
        )


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
