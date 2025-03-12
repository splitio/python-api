from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict


class HarnessGroup(BaseResource):
    '''
    HarnessGroup resource representing a Harness group
    '''
    _schema = {
    "accountIdentifier": "string",
    "orgIdentifier": "string",
    "projectIdentifier": "string",
    "identifier": "string",
    "name": "string",
    "users": [
      {
        "uuid": "string",
        "name": "string",
        "email": "string",
        "token": "string",
        "defaultAccountId": "string",
        "intent": "string",
        "accounts": [
          {
            "uuid": "string",
            "accountName": "string",
            "companyName": "string",
            "defaultExperience": "NG",
            "createdFromNG": "boolean",
            "nextGenEnabled": "boolean"
          }
        ],
        "admin": "boolean",
        "twoFactorAuthenticationEnabled": "boolean",
        "emailVerified": "boolean",
        "locked": "boolean",
        "disabled": "boolean",
        "signupAction": "string",
        "edition": "string",
        "billingFrequency": "string",
        "utmInfo": {
          "utmSource": "string",
          "utmContent": "string",
          "utmMedium": "string",
          "utmTerm": "string",
          "utmCampaign": "string"
        },
        "externallyManaged": "boolean",
        "givenName": "string",
        "familyName": "string",
        "externalId": "string",
        "createdAt": 'number',
        "lastUpdatedAt": 'number',
        "userPreferences": {
          "property1": "string",
          "property2": "string"
        },
        "isEnrichedInfoCollected": "boolean",
        "lastLogin": 'number'
      }
    ],
    "notificationConfigs": [
      {
        "type": "string"
      }
    ],
    "linkedSsoId": "string",
    "linkedSsoDisplayName": "string",
    "ssoGroupId": "string",
    "ssoGroupName": "string",
    "linkedSsoType": "string",
    "externallyManaged": "boolean",
    "description": "string",
    "tags": {
      "property1": "string",
      "property2": "string"
    },
    "harnessManaged": "boolean",
    "ssoLinked": "boolean"
  }
    def __init__(self, data=None, client=None):
        '''
        Initialize a HarnessGroup resource
        
        :param data: Dictionary containing group data
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

    @property
    def name(self):
        '''
        Get the group name
        
        :returns: Group name
        :rtype: str
        '''
        return self._name
        
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
        Export the group as a dictionary
        
        :returns: Group data as a dictionary
        :rtype: dict
        '''
        # Export properties based on schema
        schema_data_fields = self._schema.get('data', {}).keys()
        return {
            field: getattr(self, f"_{field}")
            for field in schema_data_fields
        }
