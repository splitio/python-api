from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class Token(BaseResource):
    '''
    Token resource representing a Harness authentication token
    '''
    _schema = {
        "identifier": "string",
        "name": "string",
        "validFrom": "number",
        "validTo": "number",
        "scheduledExpireTime": "number",
        "valid": "boolean",
        "accountIdentifier": "string",
        "projectIdentifier": "string",
        "orgIdentifier": "string",
        "apiKeyIdentifier": "string",
        "parentIdentifier": "string",
        "apiKeyType": "USER",
        "description": "string",
        "tags": {
            "property1": "string",
            "property2": "string"
        },
        "sshKeyContent": "string",
        "sshKeyUsage": [
            "AUTH"
        ]
        }

    def __init__(self, data=None, client=None):
        '''
        Initialize a Token resource
        
        :param data: Dictionary containing token data
        :param client: HTTP client for making API requests
        '''
        if not data:
            data = {}
        # Initialize BaseResource with identifier
        BaseResource.__init__(self, data.get('identifier'), client)
        
        # Dynamically set properties based on schema
        schema_data_fields = self._schema.get('data', {}).keys()
        for field in schema_data_fields:
            # Convert camelCase to snake_case for property names
            snake_field = ''.join(['_' + c.lower() if c.isupper() else c for c in field]).lstrip('_')
            setattr(self, f"_{snake_field}", data.get(field))
        
    def __getattr__(self, name):
        '''
        Dynamic getter for properties based on schema fields
        
        :param name: Property name
        :returns: Property value
        :raises: AttributeError if property doesn't exist
        '''
        # Check if this is a property defined in the schema
        snake_field = name
        if name in self._schema.get('data', {}).keys():
            attr_name = f"_{snake_field}"
            if hasattr(self, attr_name):
                return getattr(self, attr_name)
        
        # If not found, raise AttributeError
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def export_dict(self):
        '''
        Export the token as a dictionary
        
        :returns: Token data as a dictionary
        :rtype: dict
        '''
        # Export properties based on schema
        schema_data_fields = self._schema.get('data', {}).keys()
        return {
            field: getattr(self, f"_{field}")
            for field in schema_data_fields
        }

