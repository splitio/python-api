from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class ResourceGroup(BaseResource):
    '''
    ResourceGroup resource representing a Harness resource group
    '''
    _schema = {

      "accountIdentifier": "string",
      "orgIdentifier": "string",
      "projectIdentifier": "string",
      "identifier": "string",
      "name": "string",
      "color": "string",
      "tags": {
        "property1": "string",
        "property2": "string"
      },
      "description": "string",
      "allowedScopeLevels": [
        "string"
      ],
      "includedScopes": [
        {
          "filter": "EXCLUDING_CHILD_SCOPES",
          "accountIdentifier": "string",
          "orgIdentifier": "string",
          "projectIdentifier": "string"
        }
      ],
      "resourceFilter": {
        "resources": [
          {
            "resourceType": "string",
            "identifiers": [
              "string"
            ],
            "attributeFilter": {
              "attributeName": "string",
              "attributeValues": [
                null
              ]
            }
          }
        ],
        "includeAllResources": true
      }
    }
   
    def __init__(self, data=None, client=None):
        '''
        Initialize a ResourceGroup resource
        
        :param data: Dictionary containing resource group data
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
        Export the resource group as a dictionary
        
        :returns: Resource group data as a dictionary
        :rtype: dict
        '''
        # Export properties based on schema
        schema_data_fields = self._schema.get('data', {}).keys()
        return {
            field: getattr(self, f"_{field}")
            for field in schema_data_fields
        }