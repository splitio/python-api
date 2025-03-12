from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class HarnessProject(BaseResource):
    '''
    HarnessProject resource representing a Harness project
    '''
    _schema = {
      "orgIdentifier": "string",
      "identifier": "string",
      "name": "string",
      "color": "string",
      "modules": [
        "string"
      ],
      "description": "string",
      "tags": {
        "property1": "string",
        "property2": "string"
      }
    }

    def __init__(self, data=None, client=None):
        '''
        Initialize a HarnessProject resource
        
        :param data: Dictionary containing project data
        :param client: HTTP client for making API requests
        '''
        if not data:
            data = {}
        # Initialize BaseResource with identifier
        BaseResource.__init__(self, data.get('identifier'), client)
        
        # Dynamically set properties based on schema
        for field in self._schema.keys():
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
        camel_field = ''.join([c.capitalize() if i > 0 else c for i, c in enumerate(name.split('_'))])
        if camel_field in self._schema.keys():
            attr_name = f"_{name}"
            if hasattr(self, attr_name):
                return getattr(self, attr_name)
        
        # If not found, raise AttributeError
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def export_dict(self):
        '''
        Export the project as a dictionary
        
        :returns: Project data as a dictionary
        :rtype: dict
        '''
        result = {}
        for field in self._schema.keys():
            # Convert schema field (camelCase) to attribute name (snake_case)
            snake_field = ''.join(['_' + c.lower() if c.isupper() else c for c in field]).lstrip('_')
            attr_name = f"_{snake_field}"
            if hasattr(self, attr_name):
                result[field] = getattr(self, attr_name)
        return result
