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


    def __getattr__(self, name):
        '''
        Dynamic getter for properties based on schema fields
        
        :param name: Property name
        :returns: Property value
        :raises: AttributeError if property doesn't exist
        '''
        # Convert camelCase to snake_case
        snake_field = ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
        
        # Check if this is a property defined in the schema
        for schema_field in self._schema.keys():
            # Try direct match with schema field
            if name == schema_field:
                attr_name = f"_{snake_field}"
                if hasattr(self, attr_name):
                    return getattr(self, attr_name)
            
            # Try snake_case version of schema field
            schema_snake = ''.join(['_' + c.lower() if c.isupper() else c for c in schema_field]).lstrip('_')
            if name == schema_snake:
                attr_name = f"_{schema_snake}"
                if hasattr(self, attr_name):
                    return getattr(self, attr_name)
        
        # If not found, raise AttributeError
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def export_dict(self):
        '''
        Export the API key as a dictionary
        
        :returns: API key data as a dictionary
        :rtype: dict
        '''
        # Export properties based on schema
        result = {}
        for field in self._schema.keys():
            # Convert camelCase to snake_case for attribute lookup
            snake_field = ''.join(['_' + c.lower() if c.isupper() else c for c in field]).lstrip('_')
            attr_name = f"_{snake_field}"
            if hasattr(self, attr_name):
                result[field] = getattr(self, attr_name)
        return result
