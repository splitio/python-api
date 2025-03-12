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
      "governanceMetadata": {
        "unknownFields": {
          "initialized": true,
          "serializedSize": 0,
          "parserForType": {},
          "defaultInstanceForType": {},
          "serializedSizeAsMessageSet": 0
        },
        "message": "string",
        "id": "string",
        "type": "string",
        "timestamp": 0,
        "initialized": true,
        "status": "string",
        "action": "string",
        "entity": "string",
        "detailsList": [
          {
            "unknownFields": {
              "initialized": true,
              "serializedSize": 0,
              "parserForType": {},
              "defaultInstanceForType": {},
              "serializedSizeAsMessageSet": 0
            },
            "initialized": true,
            "identifier": "string",
            "description": "string",
            "status": "string",
            "policyMetadataList": [
              {
                "unknownFields": null,
                "severity": null,
                "initialized": null,
                "identifier": null,
                "status": null,
                "error": null,
                "identifierBytes": null,
                "defaultInstanceForType": null,
                "policyId": null,
                "policyIdBytes": null,
                "policyName": null,
                "policyNameBytes": null,
                "severityBytes": null,
                "denyMessagesList": [],
                "denyMessagesCount": null,
                "statusBytes": null,
                "accountId": null,
                "accountIdBytes": null,
                "orgId": null,
                "orgIdBytes": null,
                "projectId": null,
                "projectIdBytes": null,
                "created": null,
                "updated": null,
                "errorBytes": null,
                "serializedSize": null,
                "parserForType": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              }
            ],
            "policyMetadataCount": 0,
            "policyMetadataOrBuilderList": [
              {
                "severity": null,
                "identifier": null,
                "status": null,
                "error": null,
                "identifierBytes": null,
                "policyIdBytes": null,
                "policyName": null,
                "policyNameBytes": null,
                "severityBytes": null,
                "denyMessagesList": [],
                "denyMessagesCount": null,
                "statusBytes": null,
                "accountId": null,
                "accountIdBytes": null,
                "orgId": null,
                "orgIdBytes": null,
                "projectId": null,
                "projectIdBytes": null,
                "created": null,
                "updated": null,
                "errorBytes": null,
                "policyId": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "defaultInstanceForType": null,
                "initialized": null
              }
            ],
            "policySetName": "string",
            "policySetNameBytes": {
              "empty": true,
              "validUtf8": true
            },
            "descriptionBytes": {
              "empty": true,
              "validUtf8": true
            },
            "identifierBytes": {
              "empty": true,
              "validUtf8": true
            },
            "defaultInstanceForType": {},
            "statusBytes": {
              "empty": true,
              "validUtf8": true
            },
            "accountId": "string",
            "accountIdBytes": {
              "empty": true,
              "validUtf8": true
            },
            "orgId": "string",
            "orgIdBytes": {
              "empty": true,
              "validUtf8": true
            },
            "projectId": "string",
            "projectIdBytes": {
              "empty": true,
              "validUtf8": true
            },
            "created": 0,
            "policySetId": "string",
            "policySetIdBytes": {
              "empty": true,
              "validUtf8": true
            },
            "deny": true,
            "serializedSize": 0,
            "parserForType": {},
            "allFields": {
              "property1": {},
              "property2": {}
            },
            "descriptorForType": {
              "index": 0,
              "proto": {
                "unknownFields": null,
                "name": null,
                "initialized": null,
                "options": null,
                "fieldCount": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "enumTypeCount": null,
                "extensionCount": null,
                "reservedRangeList": [],
                "reservedNameList": [],
                "extensionRangeList": [],
                "oneofDeclCount": null,
                "nestedTypeCount": null,
                "extensionRangeCount": null,
                "enumTypeList": [],
                "enumTypeOrBuilderList": [],
                "extensionList": [],
                "extensionOrBuilderList": [],
                "optionsOrBuilder": null,
                "nameBytes": null,
                "fieldList": [],
                "fieldOrBuilderList": [],
                "nestedTypeList": [],
                "nestedTypeOrBuilderList": [],
                "extensionRangeOrBuilderList": [],
                "oneofDeclList": [],
                "oneofDeclOrBuilderList": [],
                "reservedRangeCount": null,
                "reservedRangeOrBuilderList": [],
                "reservedNameCount": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              },
              "fullName": "string",
              "file": {
                "proto": null,
                "messageTypes": [],
                "enumTypes": [],
                "services": [],
                "extensions": [],
                "dependencies": [],
                "publicDependencies": [],
                "name": null,
                "package": null,
                "file": null,
                "fullName": null,
                "options": null,
                "syntax": null,
                "edition": null,
                "editionName": null
              },
              "containingType": {},
              "nestedTypes": [
                null
              ],
              "enumTypes": [
                null
              ],
              "fields": [
                null
              ],
              "extensions": [
                null
              ],
              "oneofs": [
                null
              ],
              "name": "string",
              "options": {
                "unknownFields": null,
                "initialized": null,
                "features": null,
                "messageSetWireFormat": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "deprecated": null,
                "featuresOrBuilder": null,
                "uninterpretedOptionList": [],
                "uninterpretedOptionCount": null,
                "uninterpretedOptionOrBuilderList": [],
                "mapEntry": null,
                "noStandardDescriptorAccessor": null,
                "deprecatedLegacyJsonFieldConflicts": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "allFieldsRaw": {},
                "memoizedSerializedSize": null
              },
              "realOneofs": [
                null
              ],
              "extendable": true
            },
            "initializationErrorString": "string"
          }
        ],
        "idBytes": {
          "empty": true,
          "validUtf8": true
        },
        "detailsCount": 0,
        "detailsOrBuilderList": [
          {
            "identifier": "string",
            "description": "string",
            "status": "string",
            "policyMetadataList": [
              {
                "unknownFields": null,
                "severity": null,
                "initialized": null,
                "identifier": null,
                "status": null,
                "error": null,
                "identifierBytes": null,
                "defaultInstanceForType": null,
                "policyId": null,
                "policyIdBytes": null,
                "policyName": null,
                "policyNameBytes": null,
                "severityBytes": null,
                "denyMessagesList": [],
                "denyMessagesCount": null,
                "statusBytes": null,
                "accountId": null,
                "accountIdBytes": null,
                "orgId": null,
                "orgIdBytes": null,
                "projectId": null,
                "projectIdBytes": null,
                "created": null,
                "updated": null,
                "errorBytes": null,
                "serializedSize": null,
                "parserForType": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              }
            ],
            "policyMetadataCount": 0,
            "policyMetadataOrBuilderList": [
              {
                "severity": null,
                "identifier": null,
                "status": null,
                "error": null,
                "identifierBytes": null,
                "policyIdBytes": null,
                "policyName": null,
                "policyNameBytes": null,
                "severityBytes": null,
                "denyMessagesList": [],
                "denyMessagesCount": null,
                "statusBytes": null,
                "accountId": null,
                "accountIdBytes": null,
                "orgId": null,
                "orgIdBytes": null,
                "projectId": null,
                "projectIdBytes": null,
                "created": null,
                "updated": null,
                "errorBytes": null,
                "policyId": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "defaultInstanceForType": null,
                "initialized": null
              }
            ],
            "policySetName": "string",
            "policySetNameBytes": {
              "empty": true,
              "validUtf8": true
            },
            "descriptionBytes": {
              "empty": true,
              "validUtf8": true
            },
            "identifierBytes": {
              "empty": true,
              "validUtf8": true
            },
            "statusBytes": {
              "empty": true,
              "validUtf8": true
            },
            "accountId": "string",
            "accountIdBytes": {
              "empty": true,
              "validUtf8": true
            },
            "orgId": "string",
            "orgIdBytes": {
              "empty": true,
              "validUtf8": true
            },
            "projectId": "string",
            "projectIdBytes": {
              "empty": true,
              "validUtf8": true
            },
            "created": 0,
            "policySetId": "string",
            "policySetIdBytes": {
              "empty": true,
              "validUtf8": true
            },
            "deny": true,
            "allFields": {
              "property1": {},
              "property2": {}
            },
            "descriptorForType": {
              "index": 0,
              "proto": {
                "unknownFields": null,
                "name": null,
                "initialized": null,
                "options": null,
                "fieldCount": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "enumTypeCount": null,
                "extensionCount": null,
                "reservedRangeList": [],
                "reservedNameList": [],
                "extensionRangeList": [],
                "oneofDeclCount": null,
                "nestedTypeCount": null,
                "extensionRangeCount": null,
                "enumTypeList": [],
                "enumTypeOrBuilderList": [],
                "extensionList": [],
                "extensionOrBuilderList": [],
                "optionsOrBuilder": null,
                "nameBytes": null,
                "fieldList": [],
                "fieldOrBuilderList": [],
                "nestedTypeList": [],
                "nestedTypeOrBuilderList": [],
                "extensionRangeOrBuilderList": [],
                "oneofDeclList": [],
                "oneofDeclOrBuilderList": [],
                "reservedRangeCount": null,
                "reservedRangeOrBuilderList": [],
                "reservedNameCount": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              },
              "fullName": "string",
              "file": {
                "proto": null,
                "messageTypes": [],
                "enumTypes": [],
                "services": [],
                "extensions": [],
                "dependencies": [],
                "publicDependencies": [],
                "name": null,
                "package": null,
                "file": null,
                "fullName": null,
                "options": null,
                "syntax": null,
                "edition": null,
                "editionName": null
              },
              "containingType": {},
              "nestedTypes": [
                null
              ],
              "enumTypes": [
                null
              ],
              "fields": [
                null
              ],
              "extensions": [
                null
              ],
              "oneofs": [
                null
              ],
              "name": "string",
              "options": {
                "unknownFields": null,
                "initialized": null,
                "features": null,
                "messageSetWireFormat": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "deprecated": null,
                "featuresOrBuilder": null,
                "uninterpretedOptionList": [],
                "uninterpretedOptionCount": null,
                "uninterpretedOptionOrBuilderList": [],
                "mapEntry": null,
                "noStandardDescriptorAccessor": null,
                "deprecatedLegacyJsonFieldConflicts": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "allFieldsRaw": {},
                "memoizedSerializedSize": null
              },
              "realOneofs": [
                null
              ],
              "extendable": true
            },
            "defaultInstanceForType": {
              "parserForType": {},
              "serializedSize": 0,
              "initialized": true,
              "defaultInstanceForType": {
                "serializedSize": null,
                "parserForType": null,
                "initialized": null,
                "defaultInstanceForType": null
              },
              "allFields": {
                "property1": {},
                "property2": {}
              },
              "descriptorForType": {
                "index": null,
                "proto": null,
                "fullName": null,
                "file": null,
                "containingType": null,
                "nestedTypes": [],
                "enumTypes": [],
                "fields": [],
                "extensions": [],
                "oneofs": [],
                "name": null,
                "options": null,
                "realOneofs": [],
                "extendable": null
              },
              "initializationErrorString": "string",
              "unknownFields": {
                "initialized": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "serializedSizeAsMessageSet": null
              }
            },
            "initializationErrorString": "string",
            "unknownFields": {
              "initialized": true,
              "serializedSize": 0,
              "parserForType": {},
              "defaultInstanceForType": {},
              "serializedSizeAsMessageSet": 0
            },
            "initialized": true
          }
        ],
        "entityBytes": {
          "empty": true,
          "validUtf8": true
        },
        "actionBytes": {
          "empty": true,
          "validUtf8": true
        },
        "messageBytes": {
          "empty": true,
          "validUtf8": true
        },
        "typeBytes": {
          "empty": true,
          "validUtf8": true
        },
        "defaultInstanceForType": {},
        "statusBytes": {
          "empty": true,
          "validUtf8": true
        },
        "accountId": "string",
        "accountIdBytes": {
          "empty": true,
          "validUtf8": true
        },
        "orgId": "string",
        "orgIdBytes": {
          "empty": true,
          "validUtf8": true
        },
        "projectId": "string",
        "projectIdBytes": {
          "empty": true,
          "validUtf8": true
        },
        "created": 0,
        "deny": true,
        "serializedSize": 0,
        "parserForType": {},
        "allFields": {
          "property1": {},
          "property2": {}
        },
        "descriptorForType": {
          "index": 0,
          "proto": {
            "unknownFields": {
              "initialized": true,
              "serializedSize": 0,
              "parserForType": {},
              "defaultInstanceForType": {},
              "serializedSizeAsMessageSet": 0
            },
            "name": "string",
            "initialized": true,
            "options": {
              "unknownFields": {
                "initialized": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "serializedSizeAsMessageSet": null
              },
              "initialized": true,
              "features": {
                "unknownFields": null,
                "initialized": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "enumType": null,
                "fieldPresence": null,
                "repeatedFieldEncoding": null,
                "messageEncoding": null,
                "utf8Validation": null,
                "jsonFormat": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "allFieldsRaw": {},
                "memoizedSerializedSize": null
              },
              "messageSetWireFormat": true,
              "serializedSize": 0,
              "parserForType": {},
              "defaultInstanceForType": {},
              "deprecated": true,
              "featuresOrBuilder": {
                "enumType": null,
                "fieldPresence": null,
                "repeatedFieldEncoding": null,
                "messageEncoding": null,
                "utf8Validation": null,
                "jsonFormat": null,
                "defaultInstanceForType": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "initialized": null
              },
              "uninterpretedOptionList": [
                null
              ],
              "uninterpretedOptionCount": 0,
              "uninterpretedOptionOrBuilderList": [
                null
              ],
              "mapEntry": true,
              "noStandardDescriptorAccessor": true,
              "deprecatedLegacyJsonFieldConflicts": true,
              "allFields": {
                "property1": {},
                "property2": {}
              },
              "descriptorForType": {},
              "initializationErrorString": "string",
              "allFieldsRaw": {
                "property1": {},
                "property2": {}
              }
            },
            "fieldCount": 0,
            "serializedSize": 0,
            "parserForType": {},
            "defaultInstanceForType": {},
            "enumTypeCount": 0,
            "extensionCount": 0,
            "reservedRangeList": [
              {
                "unknownFields": null,
                "initialized": null,
                "start": null,
                "end": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              }
            ],
            "reservedNameList": [
              "string"
            ],
            "extensionRangeList": [
              {
                "unknownFields": null,
                "initialized": null,
                "options": null,
                "start": null,
                "end": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "optionsOrBuilder": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              }
            ],
            "oneofDeclCount": 0,
            "nestedTypeCount": 0,
            "extensionRangeCount": 0,
            "enumTypeList": [
              {
                "unknownFields": null,
                "name": null,
                "initialized": null,
                "options": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "reservedRangeList": [],
                "reservedNameList": [],
                "optionsOrBuilder": null,
                "nameBytes": null,
                "reservedRangeCount": null,
                "reservedRangeOrBuilderList": [],
                "reservedNameCount": null,
                "valueCount": null,
                "valueOrBuilderList": [],
                "valueList": [],
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              }
            ],
            "enumTypeOrBuilderList": [
              {
                "name": null,
                "options": null,
                "reservedRangeList": [],
                "reservedNameList": [],
                "optionsOrBuilder": null,
                "nameBytes": null,
                "reservedRangeCount": null,
                "reservedRangeOrBuilderList": [],
                "reservedNameCount": null,
                "valueCount": null,
                "valueOrBuilderList": [],
                "valueList": [],
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "defaultInstanceForType": null,
                "initialized": null
              }
            ],
            "extensionList": [
              {
                "unknownFields": null,
                "name": null,
                "typeName": null,
                "type": null,
                "defaultValue": null,
                "number": null,
                "label": null,
                "initialized": null,
                "options": null,
                "typeNameBytes": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "optionsOrBuilder": null,
                "nameBytes": null,
                "jsonName": null,
                "proto3Optional": null,
                "oneofIndex": null,
                "extendee": null,
                "extendeeBytes": null,
                "defaultValueBytes": null,
                "jsonNameBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              }
            ],
            "extensionOrBuilderList": [
              {
                "name": null,
                "typeName": null,
                "type": null,
                "defaultValue": null,
                "number": null,
                "label": null,
                "options": null,
                "typeNameBytes": null,
                "optionsOrBuilder": null,
                "nameBytes": null,
                "jsonName": null,
                "proto3Optional": null,
                "oneofIndex": null,
                "extendee": null,
                "extendeeBytes": null,
                "defaultValueBytes": null,
                "jsonNameBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "defaultInstanceForType": null,
                "initialized": null
              }
            ],
            "optionsOrBuilder": {
              "features": {
                "unknownFields": null,
                "initialized": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "enumType": null,
                "fieldPresence": null,
                "repeatedFieldEncoding": null,
                "messageEncoding": null,
                "utf8Validation": null,
                "jsonFormat": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "allFieldsRaw": {},
                "memoizedSerializedSize": null
              },
              "messageSetWireFormat": true,
              "deprecated": true,
              "featuresOrBuilder": {
                "enumType": null,
                "fieldPresence": null,
                "repeatedFieldEncoding": null,
                "messageEncoding": null,
                "utf8Validation": null,
                "jsonFormat": null,
                "defaultInstanceForType": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "initialized": null
              },
              "uninterpretedOptionList": [
                null
              ],
              "uninterpretedOptionCount": 0,
              "uninterpretedOptionOrBuilderList": [
                null
              ],
              "mapEntry": true,
              "noStandardDescriptorAccessor": true,
              "deprecatedLegacyJsonFieldConflicts": true,
              "defaultInstanceForType": {
                "parserForType": null,
                "serializedSize": null,
                "initialized": null,
                "defaultInstanceForType": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null
              },
              "allFields": {
                "property1": {},
                "property2": {}
              },
              "descriptorForType": {},
              "initializationErrorString": "string",
              "unknownFields": {
                "initialized": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "serializedSizeAsMessageSet": null
              },
              "initialized": true
            },
            "nameBytes": {
              "empty": true,
              "validUtf8": true
            },
            "fieldList": [
              {
                "unknownFields": null,
                "name": null,
                "typeName": null,
                "type": null,
                "defaultValue": null,
                "number": null,
                "label": null,
                "initialized": null,
                "options": null,
                "typeNameBytes": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "optionsOrBuilder": null,
                "nameBytes": null,
                "jsonName": null,
                "proto3Optional": null,
                "oneofIndex": null,
                "extendee": null,
                "extendeeBytes": null,
                "defaultValueBytes": null,
                "jsonNameBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              }
            ],
            "fieldOrBuilderList": [
              {
                "name": null,
                "typeName": null,
                "type": null,
                "defaultValue": null,
                "number": null,
                "label": null,
                "options": null,
                "typeNameBytes": null,
                "optionsOrBuilder": null,
                "nameBytes": null,
                "jsonName": null,
                "proto3Optional": null,
                "oneofIndex": null,
                "extendee": null,
                "extendeeBytes": null,
                "defaultValueBytes": null,
                "jsonNameBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "defaultInstanceForType": null,
                "initialized": null
              }
            ],
            "nestedTypeList": [
              {}
            ],
            "nestedTypeOrBuilderList": [
              {
                "name": null,
                "options": null,
                "fieldCount": null,
                "enumTypeCount": null,
                "extensionCount": null,
                "reservedRangeList": [],
                "reservedNameList": [],
                "extensionRangeList": [],
                "oneofDeclCount": null,
                "nestedTypeCount": null,
                "extensionRangeCount": null,
                "enumTypeList": [],
                "enumTypeOrBuilderList": [],
                "extensionList": [],
                "extensionOrBuilderList": [],
                "optionsOrBuilder": null,
                "nameBytes": null,
                "fieldList": [],
                "fieldOrBuilderList": [],
                "extensionRangeOrBuilderList": [],
                "oneofDeclList": [],
                "oneofDeclOrBuilderList": [],
                "reservedRangeCount": null,
                "reservedRangeOrBuilderList": [],
                "reservedNameCount": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "defaultInstanceForType": null,
                "initialized": null
              }
            ],
            "extensionRangeOrBuilderList": [
              {
                "options": null,
                "start": null,
                "end": null,
                "optionsOrBuilder": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "defaultInstanceForType": null,
                "initialized": null
              }
            ],
            "oneofDeclList": [
              {
                "unknownFields": null,
                "name": null,
                "initialized": null,
                "options": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "optionsOrBuilder": null,
                "nameBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              }
            ],
            "oneofDeclOrBuilderList": [
              {
                "name": null,
                "options": null,
                "optionsOrBuilder": null,
                "nameBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "defaultInstanceForType": null,
                "initialized": null
              }
            ],
            "reservedRangeCount": 0,
            "reservedRangeOrBuilderList": [
              {
                "start": null,
                "end": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "defaultInstanceForType": null,
                "initialized": null
              }
            ],
            "reservedNameCount": 0,
            "allFields": {
              "property1": {},
              "property2": {}
            },
            "descriptorForType": {},
            "initializationErrorString": "string"
          },
          "fullName": "string",
          "file": {
            "proto": {
              "unknownFields": {
                "initialized": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "serializedSizeAsMessageSet": null
              },
              "name": "string",
              "package": "string",
              "initialized": true,
              "options": {
                "unknownFields": null,
                "initialized": null,
                "features": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "javaPackageBytes": null,
                "javaOuterClassname": null,
                "javaOuterClassnameBytes": null,
                "javaMultipleFiles": null,
                "javaGenerateEqualsAndHash": null,
                "javaStringCheckUtf8": null,
                "optimizeFor": null,
                "goPackage": null,
                "goPackageBytes": null,
                "ccGenericServices": null,
                "javaGenericServices": null,
                "pyGenericServices": null,
                "phpGenericServices": null,
                "deprecated": null,
                "ccEnableArenas": null,
                "javaPackage": null,
                "objcClassPrefix": null,
                "objcClassPrefixBytes": null,
                "csharpNamespace": null,
                "csharpNamespaceBytes": null,
                "swiftPrefix": null,
                "swiftPrefixBytes": null,
                "phpClassPrefix": null,
                "phpClassPrefixBytes": null,
                "phpNamespace": null,
                "phpNamespaceBytes": null,
                "phpMetadataNamespace": null,
                "phpMetadataNamespaceBytes": null,
                "rubyPackage": null,
                "rubyPackageBytes": null,
                "featuresOrBuilder": null,
                "uninterpretedOptionList": [],
                "uninterpretedOptionCount": null,
                "uninterpretedOptionOrBuilderList": [],
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "allFieldsRaw": {},
                "memoizedSerializedSize": null
              },
              "syntax": "string",
              "edition": "EDITION_UNKNOWN",
              "serializedSize": 0,
              "parserForType": {},
              "defaultInstanceForType": {},
              "publicDependencyCount": 0,
              "dependencyCount": 0,
              "messageTypeCount": 0,
              "enumTypeCount": 0,
              "serviceCount": 0,
              "extensionCount": 0,
              "packageBytes": {
                "empty": null,
                "validUtf8": null
              },
              "dependencyList": [
                null
              ],
              "publicDependencyList": [
                null
              ],
              "weakDependencyList": [
                null
              ],
              "weakDependencyCount": 0,
              "messageTypeList": [
                null
              ],
              "messageTypeOrBuilderList": [
                null
              ],
              "enumTypeList": [
                null
              ],
              "enumTypeOrBuilderList": [
                null
              ],
              "serviceList": [
                null
              ],
              "serviceOrBuilderList": [
                null
              ],
              "extensionList": [
                null
              ],
              "extensionOrBuilderList": [
                null
              ],
              "optionsOrBuilder": {
                "features": null,
                "javaPackageBytes": null,
                "javaOuterClassname": null,
                "javaOuterClassnameBytes": null,
                "javaMultipleFiles": null,
                "javaGenerateEqualsAndHash": null,
                "javaStringCheckUtf8": null,
                "optimizeFor": null,
                "goPackage": null,
                "goPackageBytes": null,
                "ccGenericServices": null,
                "javaGenericServices": null,
                "pyGenericServices": null,
                "phpGenericServices": null,
                "deprecated": null,
                "ccEnableArenas": null,
                "javaPackage": null,
                "objcClassPrefix": null,
                "objcClassPrefixBytes": null,
                "csharpNamespace": null,
                "csharpNamespaceBytes": null,
                "swiftPrefix": null,
                "swiftPrefixBytes": null,
                "phpClassPrefix": null,
                "phpClassPrefixBytes": null,
                "phpNamespace": null,
                "phpNamespaceBytes": null,
                "phpMetadataNamespace": null,
                "phpMetadataNamespaceBytes": null,
                "rubyPackage": null,
                "rubyPackageBytes": null,
                "featuresOrBuilder": null,
                "uninterpretedOptionList": [],
                "uninterpretedOptionCount": null,
                "uninterpretedOptionOrBuilderList": [],
                "defaultInstanceForType": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "initialized": null
              },
              "sourceCodeInfo": {
                "unknownFields": null,
                "initialized": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "locationCount": null,
                "locationOrBuilderList": [],
                "locationList": [],
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              },
              "sourceCodeInfoOrBuilder": {
                "locationCount": null,
                "locationOrBuilderList": [],
                "locationList": [],
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "defaultInstanceForType": null,
                "initialized": null
              },
              "syntaxBytes": {
                "empty": null,
                "validUtf8": null
              },
              "nameBytes": {
                "empty": null,
                "validUtf8": null
              },
              "allFields": {
                "property1": {},
                "property2": {}
              },
              "descriptorForType": {},
              "initializationErrorString": "string"
            },
            "messageTypes": [
              {}
            ],
            "enumTypes": [
              {
                "index": null,
                "proto": null,
                "fullName": null,
                "file": null,
                "containingType": null,
                "values": [],
                "name": null,
                "options": null,
                "closed": null
              }
            ],
            "services": [
              {
                "index": null,
                "proto": null,
                "fullName": null,
                "file": null,
                "methods": [],
                "name": null,
                "options": null
              }
            ],
            "extensions": [
              {
                "index": null,
                "proto": null,
                "fullName": null,
                "jsonName": null,
                "file": null,
                "extensionScope": null,
                "type": null,
                "containingType": null,
                "messageType": null,
                "containingOneof": null,
                "enumType": null,
                "defaultValue": {},
                "name": null,
                "number": null,
                "options": null,
                "required": null,
                "optional": null,
                "repeated": null,
                "mapField": null,
                "javaType": null,
                "extension": null,
                "liteType": null,
                "liteJavaType": null,
                "packed": null,
                "packable": null,
                "realContainingOneof": null
              }
            ],
            "dependencies": [
              {}
            ],
            "publicDependencies": [
              {}
            ],
            "name": "string",
            "package": "string",
            "file": {},
            "fullName": "string",
            "options": {
              "unknownFields": {
                "initialized": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "serializedSizeAsMessageSet": null
              },
              "initialized": true,
              "features": {
                "unknownFields": null,
                "initialized": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "enumType": null,
                "fieldPresence": null,
                "repeatedFieldEncoding": null,
                "messageEncoding": null,
                "utf8Validation": null,
                "jsonFormat": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "allFieldsRaw": {},
                "memoizedSerializedSize": null
              },
              "serializedSize": 0,
              "parserForType": {},
              "defaultInstanceForType": {},
              "javaPackageBytes": {
                "empty": null,
                "validUtf8": null
              },
              "javaOuterClassname": "string",
              "javaOuterClassnameBytes": {
                "empty": null,
                "validUtf8": null
              },
              "javaMultipleFiles": true,
              "javaGenerateEqualsAndHash": true,
              "javaStringCheckUtf8": true,
              "optimizeFor": "SPEED",
              "goPackage": "string",
              "goPackageBytes": {
                "empty": null,
                "validUtf8": null
              },
              "ccGenericServices": true,
              "javaGenericServices": true,
              "pyGenericServices": true,
              "phpGenericServices": true,
              "deprecated": true,
              "ccEnableArenas": true,
              "javaPackage": "string",
              "objcClassPrefix": "string",
              "objcClassPrefixBytes": {
                "empty": null,
                "validUtf8": null
              },
              "csharpNamespace": "string",
              "csharpNamespaceBytes": {
                "empty": null,
                "validUtf8": null
              },
              "swiftPrefix": "string",
              "swiftPrefixBytes": {
                "empty": null,
                "validUtf8": null
              },
              "phpClassPrefix": "string",
              "phpClassPrefixBytes": {
                "empty": null,
                "validUtf8": null
              },
              "phpNamespace": "string",
              "phpNamespaceBytes": {
                "empty": null,
                "validUtf8": null
              },
              "phpMetadataNamespace": "string",
              "phpMetadataNamespaceBytes": {
                "empty": null,
                "validUtf8": null
              },
              "rubyPackage": "string",
              "rubyPackageBytes": {
                "empty": null,
                "validUtf8": null
              },
              "featuresOrBuilder": {
                "enumType": null,
                "fieldPresence": null,
                "repeatedFieldEncoding": null,
                "messageEncoding": null,
                "utf8Validation": null,
                "jsonFormat": null,
                "defaultInstanceForType": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "initialized": null
              },
              "uninterpretedOptionList": [
                null
              ],
              "uninterpretedOptionCount": 0,
              "uninterpretedOptionOrBuilderList": [
                null
              ],
              "allFields": {
                "property1": {},
                "property2": {}
              },
              "descriptorForType": {},
              "initializationErrorString": "string",
              "allFieldsRaw": {
                "property1": {},
                "property2": {}
              }
            },
            "syntax": "UNKNOWN",
            "edition": "EDITION_UNKNOWN",
            "editionName": "string"
          },
          "containingType": {},
          "nestedTypes": [
            {}
          ],
          "enumTypes": [
            {
              "index": 0,
              "proto": {
                "unknownFields": null,
                "name": null,
                "initialized": null,
                "options": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "reservedRangeList": [],
                "reservedNameList": [],
                "optionsOrBuilder": null,
                "nameBytes": null,
                "reservedRangeCount": null,
                "reservedRangeOrBuilderList": [],
                "reservedNameCount": null,
                "valueCount": null,
                "valueOrBuilderList": [],
                "valueList": [],
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              },
              "fullName": "string",
              "file": {
                "proto": null,
                "messageTypes": [],
                "enumTypes": [],
                "services": [],
                "extensions": [],
                "dependencies": [],
                "publicDependencies": [],
                "name": null,
                "package": null,
                "file": null,
                "fullName": null,
                "options": null,
                "syntax": null,
                "edition": null,
                "editionName": null
              },
              "containingType": {},
              "values": [
                null
              ],
              "name": "string",
              "options": {
                "unknownFields": null,
                "initialized": null,
                "features": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "deprecated": null,
                "featuresOrBuilder": null,
                "uninterpretedOptionList": [],
                "uninterpretedOptionCount": null,
                "uninterpretedOptionOrBuilderList": [],
                "deprecatedLegacyJsonFieldConflicts": null,
                "allowAlias": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "allFieldsRaw": {},
                "memoizedSerializedSize": null
              },
              "closed": true
            }
          ],
          "fields": [
            {
              "index": 0,
              "proto": {
                "unknownFields": null,
                "name": null,
                "typeName": null,
                "type": null,
                "defaultValue": null,
                "number": null,
                "label": null,
                "initialized": null,
                "options": null,
                "typeNameBytes": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "optionsOrBuilder": null,
                "nameBytes": null,
                "jsonName": null,
                "proto3Optional": null,
                "oneofIndex": null,
                "extendee": null,
                "extendeeBytes": null,
                "defaultValueBytes": null,
                "jsonNameBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              },
              "fullName": "string",
              "jsonName": "string",
              "file": {
                "proto": null,
                "messageTypes": [],
                "enumTypes": [],
                "services": [],
                "extensions": [],
                "dependencies": [],
                "publicDependencies": [],
                "name": null,
                "package": null,
                "file": null,
                "fullName": null,
                "options": null,
                "syntax": null,
                "edition": null,
                "editionName": null
              },
              "extensionScope": {},
              "type": "DOUBLE",
              "containingType": {},
              "messageType": {},
              "containingOneof": {
                "index": null,
                "proto": null,
                "fullName": null,
                "file": null,
                "containingType": null,
                "fieldCount": null,
                "fields": [],
                "name": null,
                "synthetic": null,
                "options": null
              },
              "enumType": {
                "index": null,
                "proto": null,
                "fullName": null,
                "file": null,
                "containingType": null,
                "values": [],
                "name": null,
                "options": null,
                "closed": null
              },
              "defaultValue": {},
              "name": "string",
              "number": 0,
              "options": {
                "unknownFields": null,
                "initialized": null,
                "retention": null,
                "editionDefaultsOrBuilderList": [],
                "features": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "deprecated": null,
                "featuresOrBuilder": null,
                "uninterpretedOptionList": [],
                "uninterpretedOptionCount": null,
                "uninterpretedOptionOrBuilderList": [],
                "packed": null,
                "ctype": null,
                "jstype": null,
                "lazy": null,
                "unverifiedLazy": null,
                "weak": null,
                "debugRedact": null,
                "targetsList": [],
                "targetsCount": null,
                "editionDefaultsList": [],
                "editionDefaultsCount": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "allFieldsRaw": {},
                "memoizedSerializedSize": null
              },
              "required": true,
              "optional": true,
              "repeated": true,
              "mapField": true,
              "javaType": "INT",
              "extension": true,
              "liteType": "DOUBLE",
              "liteJavaType": "INT",
              "packed": true,
              "packable": true,
              "realContainingOneof": {
                "index": null,
                "proto": null,
                "fullName": null,
                "file": null,
                "containingType": null,
                "fieldCount": null,
                "fields": [],
                "name": null,
                "synthetic": null,
                "options": null
              }
            }
          ],
          "extensions": [
            {
              "index": 0,
              "proto": {
                "unknownFields": null,
                "name": null,
                "typeName": null,
                "type": null,
                "defaultValue": null,
                "number": null,
                "label": null,
                "initialized": null,
                "options": null,
                "typeNameBytes": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "optionsOrBuilder": null,
                "nameBytes": null,
                "jsonName": null,
                "proto3Optional": null,
                "oneofIndex": null,
                "extendee": null,
                "extendeeBytes": null,
                "defaultValueBytes": null,
                "jsonNameBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              },
              "fullName": "string",
              "jsonName": "string",
              "file": {
                "proto": null,
                "messageTypes": [],
                "enumTypes": [],
                "services": [],
                "extensions": [],
                "dependencies": [],
                "publicDependencies": [],
                "name": null,
                "package": null,
                "file": null,
                "fullName": null,
                "options": null,
                "syntax": null,
                "edition": null,
                "editionName": null
              },
              "extensionScope": {},
              "type": "DOUBLE",
              "containingType": {},
              "messageType": {},
              "containingOneof": {
                "index": null,
                "proto": null,
                "fullName": null,
                "file": null,
                "containingType": null,
                "fieldCount": null,
                "fields": [],
                "name": null,
                "synthetic": null,
                "options": null
              },
              "enumType": {
                "index": null,
                "proto": null,
                "fullName": null,
                "file": null,
                "containingType": null,
                "values": [],
                "name": null,
                "options": null,
                "closed": null
              },
              "defaultValue": {},
              "name": "string",
              "number": 0,
              "options": {
                "unknownFields": null,
                "initialized": null,
                "retention": null,
                "editionDefaultsOrBuilderList": [],
                "features": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "deprecated": null,
                "featuresOrBuilder": null,
                "uninterpretedOptionList": [],
                "uninterpretedOptionCount": null,
                "uninterpretedOptionOrBuilderList": [],
                "packed": null,
                "ctype": null,
                "jstype": null,
                "lazy": null,
                "unverifiedLazy": null,
                "weak": null,
                "debugRedact": null,
                "targetsList": [],
                "targetsCount": null,
                "editionDefaultsList": [],
                "editionDefaultsCount": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "allFieldsRaw": {},
                "memoizedSerializedSize": null
              },
              "required": true,
              "optional": true,
              "repeated": true,
              "mapField": true,
              "javaType": "INT",
              "extension": true,
              "liteType": "DOUBLE",
              "liteJavaType": "INT",
              "packed": true,
              "packable": true,
              "realContainingOneof": {
                "index": null,
                "proto": null,
                "fullName": null,
                "file": null,
                "containingType": null,
                "fieldCount": null,
                "fields": [],
                "name": null,
                "synthetic": null,
                "options": null
              }
            }
          ],
          "oneofs": [
            {
              "index": 0,
              "proto": {
                "unknownFields": null,
                "name": null,
                "initialized": null,
                "options": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "optionsOrBuilder": null,
                "nameBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              },
              "fullName": "string",
              "file": {
                "proto": null,
                "messageTypes": [],
                "enumTypes": [],
                "services": [],
                "extensions": [],
                "dependencies": [],
                "publicDependencies": [],
                "name": null,
                "package": null,
                "file": null,
                "fullName": null,
                "options": null,
                "syntax": null,
                "edition": null,
                "editionName": null
              },
              "containingType": {},
              "fieldCount": 0,
              "fields": [
                null
              ],
              "name": "string",
              "synthetic": true,
              "options": {
                "unknownFields": null,
                "initialized": null,
                "features": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "featuresOrBuilder": null,
                "uninterpretedOptionList": [],
                "uninterpretedOptionCount": null,
                "uninterpretedOptionOrBuilderList": [],
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "allFieldsRaw": {},
                "memoizedSerializedSize": null
              }
            }
          ],
          "name": "string",
          "options": {
            "unknownFields": {
              "initialized": true,
              "serializedSize": 0,
              "parserForType": {},
              "defaultInstanceForType": {},
              "serializedSizeAsMessageSet": 0
            },
            "initialized": true,
            "features": {
              "unknownFields": {
                "initialized": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "serializedSizeAsMessageSet": null
              },
              "initialized": true,
              "serializedSize": 0,
              "parserForType": {},
              "defaultInstanceForType": {},
              "enumType": "ENUM_TYPE_UNKNOWN",
              "fieldPresence": "FIELD_PRESENCE_UNKNOWN",
              "repeatedFieldEncoding": "REPEATED_FIELD_ENCODING_UNKNOWN",
              "messageEncoding": "MESSAGE_ENCODING_UNKNOWN",
              "utf8Validation": "UTF8_VALIDATION_UNKNOWN",
              "jsonFormat": "JSON_FORMAT_UNKNOWN",
              "allFields": {
                "property1": {},
                "property2": {}
              },
              "descriptorForType": {},
              "initializationErrorString": "string",
              "allFieldsRaw": {
                "property1": {},
                "property2": {}
              }
            },
            "messageSetWireFormat": true,
            "serializedSize": 0,
            "parserForType": {},
            "defaultInstanceForType": {},
            "deprecated": true,
            "featuresOrBuilder": {
              "enumType": "ENUM_TYPE_UNKNOWN",
              "fieldPresence": "FIELD_PRESENCE_UNKNOWN",
              "repeatedFieldEncoding": "REPEATED_FIELD_ENCODING_UNKNOWN",
              "messageEncoding": "MESSAGE_ENCODING_UNKNOWN",
              "utf8Validation": "UTF8_VALIDATION_UNKNOWN",
              "jsonFormat": "JSON_FORMAT_UNKNOWN",
              "defaultInstanceForType": {
                "parserForType": null,
                "serializedSize": null,
                "initialized": null,
                "defaultInstanceForType": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null
              },
              "allFields": {
                "property1": {},
                "property2": {}
              },
              "descriptorForType": {},
              "initializationErrorString": "string",
              "unknownFields": {
                "initialized": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "serializedSizeAsMessageSet": null
              },
              "initialized": true
            },
            "uninterpretedOptionList": [
              {
                "unknownFields": null,
                "nameCount": null,
                "initialized": null,
                "stringValue": null,
                "doubleValue": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "nameList": [],
                "nameOrBuilderList": [],
                "identifierValue": null,
                "identifierValueBytes": null,
                "positiveIntValue": null,
                "negativeIntValue": null,
                "aggregateValue": null,
                "aggregateValueBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              }
            ],
            "uninterpretedOptionCount": 0,
            "uninterpretedOptionOrBuilderList": [
              {
                "nameCount": null,
                "stringValue": null,
                "doubleValue": null,
                "nameList": [],
                "nameOrBuilderList": [],
                "identifierValue": null,
                "identifierValueBytes": null,
                "positiveIntValue": null,
                "negativeIntValue": null,
                "aggregateValue": null,
                "aggregateValueBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "unknownFields": null,
                "defaultInstanceForType": null,
                "initialized": null
              }
            ],
            "mapEntry": true,
            "noStandardDescriptorAccessor": true,
            "deprecatedLegacyJsonFieldConflicts": true,
            "allFields": {
              "property1": {},
              "property2": {}
            },
            "descriptorForType": {},
            "initializationErrorString": "string",
            "allFieldsRaw": {
              "property1": {},
              "property2": {}
            }
          },
          "realOneofs": [
            {
              "index": 0,
              "proto": {
                "unknownFields": null,
                "name": null,
                "initialized": null,
                "options": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "optionsOrBuilder": null,
                "nameBytes": null,
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "memoizedSerializedSize": null
              },
              "fullName": "string",
              "file": {
                "proto": null,
                "messageTypes": [],
                "enumTypes": [],
                "services": [],
                "extensions": [],
                "dependencies": [],
                "publicDependencies": [],
                "name": null,
                "package": null,
                "file": null,
                "fullName": null,
                "options": null,
                "syntax": null,
                "edition": null,
                "editionName": null
              },
              "containingType": {},
              "fieldCount": 0,
              "fields": [
                null
              ],
              "name": "string",
              "synthetic": true,
              "options": {
                "unknownFields": null,
                "initialized": null,
                "features": null,
                "serializedSize": null,
                "parserForType": null,
                "defaultInstanceForType": null,
                "featuresOrBuilder": null,
                "uninterpretedOptionList": [],
                "uninterpretedOptionCount": null,
                "uninterpretedOptionOrBuilderList": [],
                "allFields": {},
                "descriptorForType": null,
                "initializationErrorString": null,
                "allFieldsRaw": {},
                "memoizedSerializedSize": null
              }
            }
          ],
          "extendable": true
        },
        "initializationErrorString": "string"
      }
    }

    def __init__(self, data=None, client=None):
        '''
        Initialize a Role resource
        
        :param data: Dictionary containing role data
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
        Export the role as a dictionary
        
        :returns: Role data as a dictionary
        :rtype: dict
        '''
        # Export properties based on schema
        schema_data_fields = self._schema.get('data', {}).keys()
        return {
            field: getattr(self, f"_{field}")
            for field in schema_data_fields
        }
