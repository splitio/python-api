from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class HarnessApiKey(BaseResource):
    '''
    HarnessApiKey resource representing a Harness API key
    '''
    _schema = {

            'identifier': 'string',
            'name': 'string',
            'description': 'string',
            'value': 'string',
            'apiKeyType': 'string',
            'parentIdentifier': 'string',
            'defaultTimeToExpireToken': 'number',
            'accountIdentifier': 'string',
            'projectIdentifier': 'string',
            'orgIdentifier': 'string',
            'governanceMetadata': 'dict'
    }

    def __init__(self, data=None, client=None):
        '''
        Initialize a HarnessApiKey resource
        
        :param data: Dictionary containing API key data
        :param client: HTTP client for making API requests
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('identifier'), client)
        self._identifier = data.get('identifier')
        self._name = data.get('name')
        self._description = data.get('description')
        self._value = data.get('value')
        self._api_key_type = data.get('apiKeyType')
        self._parent_identifier = data.get('parentIdentifier')
        self._default_time_to_expire_token = data.get('defaultTimeToExpireToken')
        self._account_identifier = data.get('accountIdentifier')
        self._project_identifier = data.get('projectIdentifier')
        self._org_identifier = data.get('orgIdentifier')
        self._governance_metadata = data.get('governanceMetadata')


    @property
    def identifier(self):
        '''
        Get the API key identifier
        
        :returns: API key identifier
        :rtype: str
        '''
        return self._identifier

    @property
    def name(self):
        '''
        Get the API key name
        
        :returns: API key name
        :rtype: str
        '''
        return self._name

    @property
    def description(self):
        '''
        Get the API key description
        
        :returns: API key description
        :rtype: str
        '''
        return self._description

    @property
    def value(self):
        '''
        Get the API key value
        
        :returns: API key value
        :rtype: str
        '''
        return self._value

    @property
    def api_key_type(self):
        '''
        Get the API key type
        
        :returns: API key type
        :rtype: str
        '''
        return self._api_key_type

    @property
    def parent_identifier(self):
        '''
        Get the parent identifier of the API key
        
        :returns: Parent identifier
        :rtype: str
        '''
        return self._parent_identifier

    @property
    def default_time_to_expire_token(self):
        '''
        Get the default time to expire token
        
        :returns: Default time to expire token
        :rtype: int
        '''
        return self._default_time_to_expire_token

    @property
    def account_identifier(self):
        '''
        Get the account identifier of the API key
        
        :returns: Account identifier
        :rtype: str
        '''
        return self._account_identifier

    @property
    def project_identifier(self):
        '''
        Get the project identifier of the API key
        
        :returns: Project identifier
        :rtype: str
        '''
        return self._project_identifier

    @property
    def org_identifier(self):
        '''
        Get the organization identifier of the API key
        
        :returns: Organization identifier
        :rtype: str
        '''
        return self._org_identifier

    @property
    def governance_metadata(self):
        '''
        Get the governance metadata of the API key
        
        :returns: Governance metadata
        :rtype: dict
        '''
        return self._governance_metadata

    @property
    def correlation_id(self):
        '''
        Get the correlation ID of the API key
        
        :returns: Correlation ID
        :rtype: str
        '''
        return self._correlation_id


    def export_dict(self):
        '''
        Export the API key as a dictionary
        
        :returns: API key data as a dictionary
        :rtype: dict
        '''
        return {

                'identifier': self._identifier,
                'name': self._name,
                'description': self._description,
                'value': self._value,
                'apiKeyType': self._api_key_type,
                'parentIdentifier': self._parent_identifier,
                'defaultTimeToExpireToken': self._default_time_to_expire_token,
                'accountIdentifier': self._account_identifier,
                'projectIdentifier': self._project_identifier,
                'orgIdentifier': self._org_identifier,
                'governanceMetadata': self._governance_metadata,
                'correlationId': self._correlation_id
            }

