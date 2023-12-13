from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import SplitDefinitionMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources import Environment
def object_to_stringified_dict(obj):
    """
    Recursively converts an object and its nested objects to a stringified dictionary.
    Assumes that the object has a 'to_dict()' method for serialization.
    
    Args:
        obj: The object to be converted to a stringified dictionary.
        
    Returns:
        A stringified dictionary representation of the object.
    """
    if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
        return object_to_stringified_dict(obj.to_dict())  # Recursively call to_dict()
    elif isinstance(obj, dict):
        return {key: object_to_stringified_dict(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [object_to_stringified_dict(item) for item in obj]
    else:
        return obj  # For non-dict, non-list, and non-object types, return as is

class TestSplitDefinitionMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = SplitDefinitionMicroClient(sc)
        data = {'objects': [{
                'name': 'split1',
                'environment': {},
                'trafficType': {},
                'killed': False,
                'treatments': [],
                'defaultTreatment': 'off',
                'baselineTreatment': 'off',
                'trafficAllocation': 100,
                'lastTrafficReceivedAt': 0,
                'rules': [],
                'defaultRule': [],
                'creationTime': 0,
                'lastUpdateTime': 0
            }, {
                'name': 'split2',
                'environment': {},
                'trafficType': {},
                'killed': False,
                'treatments': [],
                'defaultTreatment': 'off',
                'baselineTreatment': 'off',
                'trafficAllocation': 100,
                'lastTrafficReceivedAt': 0,
                'rules': [],
                'defaultRule': [],
                'creationTime': 0,
                'lastUpdateTime': 0
            }],
            'offset': 1,
            'totalCount': 2,
            'limit': 2
        }

        SyncHttpClient.make_request.return_value = data
        result = emc.list('env_id', 'ws_id')
        SyncHttpClient.make_request.assert_called_once_with(
            SplitDefinitionMicroClient._endpoint['all_items'],
            workspaceId = 'ws_id',
            environmentId = 'env_id',
            offset = 0
        )
        data = [{
                'name': 'split1',
                'environment': Environment(data={'changePermissions': None, 'creationTime': None, 'dataExportPermissions': None, 'environmentType': None, 'workspaceIds': ['ws_id'], 'name':None, 'type': None, 'orgId': None, 'id':None, 'status':None}).to_dict(),
                'trafficType': {'displayAttributeId': None, 'id': None, 'name': None},
                'killed': False,
                'treatments': None,
                'defaultTreatment': 'off',
                'baselineTreatment': 'off',
                'trafficAllocation': 100,
                'rules': None,
                'defaultRule': None,
                'creationTime': None,
                'lastUpdateTime': None,
                'lastTrafficReceivedAt': None
            }, {
                'name': 'split2',
                'environment': Environment(data={'changePermissions': None, 'creationTime': None, 'dataExportPermissions': None, 'environmentType': None, 'workspaceIds': ['ws_id'], 'name':None, 'type': None, 'orgId': None, 'id':None, 'status':None}).to_dict(),
                'trafficType': {'displayAttributeId': None, 'id': None, 'name': None},
                'killed': False,
                'treatments': None,
                'defaultTreatment': 'off',
                'baselineTreatment': 'off',
                'trafficAllocation': 100,
                'rules': None,
                'defaultRule': None,
                'creationTime': None,
                'lastUpdateTime': None,
                'lastTrafficReceivedAt': None
            }]
        assert object_to_stringified_dict(result[0]) == data[0]
        assert object_to_stringified_dict(result[1]) == data[1]
        
    def test_get_definition(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = SplitDefinitionMicroClient(sc)
        data = {
                'name': 'split1',
                'environment': Environment(data={'changePermissions': None, 'creationTime': None, 'dataExportPermissions': None, 'environmentType': None, 'workspaceIds': ['ws_id'], 'name':None, 'type': None, 'orgId': None, 'id':None, 'status':None}).to_dict(),
                'trafficType': {'displayAttributeId': None, 'id': None, 'name': None},
                'killed': False,
                'treatments': [],
                'defaultTreatment': 'off',
                'baselineTreatment': 'off',
                'trafficAllocation': 100,
                'rules': [],
                'defaultRule': [],
                'creationTime': None,
                'lastUpdateTime': None,
                'lastTrafficReceivedAt': None
            }

        SyncHttpClient.make_request.return_value = data
        result = emc.get_definition('split1', 'env_id', 'ws_id')
        SyncHttpClient.make_request.assert_called_once_with(
            SplitDefinitionMicroClient._endpoint['get_definition'],
            workspaceId = 'ws_id',
            environmentId = 'env_id',
            splitName = 'split1'
        )
        data = {
                'name': 'split1',
                'environment': Environment(data={'changePermissions': None, 'creationTime': None, 'dataExportPermissions': None, 'environmentType': None, 'workspaceIds': ['ws_id'], 'name':None, 'type': None, 'orgId': None, 'id':None, 'status':None}).to_dict(),
                'trafficType': {'displayAttributeId': None, 'id': None, 'name': None},
                'killed': False,
                'treatments': None,
                'defaultTreatment': 'off',
                'baselineTreatment': 'off',
                'trafficAllocation': 100,
                'rules': None,
                'defaultRule': None,
                'creationTime': None,
                'lastUpdateTime': None,
                'lastTrafficReceivedAt': None
            }
        assert object_to_stringified_dict(result) == data