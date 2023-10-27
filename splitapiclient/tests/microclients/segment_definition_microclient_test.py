from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import SegmentDefinitionMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources import TrafficType

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


class TestSegmentDefinitionMicroClient:

    def test_list(self, mocker):
        '''
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        emc = SegmentDefinitionMicroClient(sc)
        data = {'objects': [{
                'name': 'name',
                'environment': {
                    'id': 'env_id',
                    'name': ''
                },
                'trafficType': {
                    'id': 'tt_id',
                    'name': 'tt'
                }},             {
                'name': 'name2',
                'environment': {
                    'id': 'env_id',
                    'name': ''
                },
                'trafficType': {
                    'id': 'tt_id',
                    'name': 'tt'
                }}
            ],
            'offset': 1,
            'totalCount': 2,
            'limit': 2
        }

        SyncHttpClient.make_request.return_value = data
        result = emc.list('env_id', 'ws_id')
        SyncHttpClient.make_request.assert_called_once_with(
            SegmentDefinitionMicroClient._endpoint['all_items'],
            workspaceId = 'ws_id',
            environmentId = 'env_id',
            offset = 0
        )
        data = [{
                'name': 'name',
                'environment': {'id': 'env_id', 'name': ''},
                'creationTime': None,
                'trafficType': TrafficType(data={"id":"tt_id", "name":"tt"}).to_dict()
                }, {
                'name': 'name2',
                'environment': {'id': 'env_id', 'name': ''},
                'creationTime': None,
                'trafficType': TrafficType(data={"id":"tt_id", "name":"tt"}).to_dict()
                }
            ]


        assert object_to_stringified_dict(result[0]) == data[0]

        assert object_to_stringified_dict(result[1]) == data[1]
