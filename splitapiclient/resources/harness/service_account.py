from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class ServiceAccount(BaseResource):
    '''
    ServiceAccount resource representing a Harness service account
    '''
    _schema = {
      "identifier": "string",
      "name": "string",
      "email": "string",
      "description": "string",
      "tags": {
        "property1": "string",
        "property2": "string"
      },
      "accountIdentifier": "string",
      "orgIdentifier": "string",
      "projectIdentifier": "string",
      "extendable": "boolean"
    }

    def __init__(self, data=None, client=None):
        '''
        Initialize a ServiceAccount resource
        
        :param data: Dictionary containing service account data
        :param client: HTTP client for making API requests
        '''
        if not data:
            data = {}
        # Initialize BaseResource with identifier
        BaseResource.__init__(self, data.get('identifier'), client)
        
        # Dynamically set properties based on schema
        schema_data_fields = self._schema.keys()
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
        Export the group as a dictionary
        
        :returns: Group data as a dictionary
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