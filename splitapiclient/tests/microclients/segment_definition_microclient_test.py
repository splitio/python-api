from __future__ import absolute_import, division, print_function, \
    unicode_literals
from unittest import mock
import pytest

from splitapiclient.microclients import SegmentDefinitionMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.resources import TrafficType, Environment

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
        
    def test_get_key_count(self, mocker):
        '''
        Test get_key_count method of SegmentDefinitionMicroClient
        '''
        # Mock the SyncHttpClient make_request method
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        
        # Create client instances
        sc = SyncHttpClient('abc', 'abc')
        segment_client = SegmentDefinitionMicroClient(sc)
        
        # Define mock response data
        mock_response = {
            'keys': [{'key': 'key1'}, {'key': 'key2'}, {'key': 'key3'}, {'key': 'key4'}, {'key': 'key5'}],
            'offset': 0,
            'count': 5,   # This is the value we expect to be returned
            'limit': 100
        }
        
        # Set the return value for the mocked method
        SyncHttpClient.make_request.return_value = mock_response
        
        # Call the method being tested
        result = segment_client.get_key_count('test_segment', 'test_env_id')
        
        # Verify the HTTP client was called with correct parameters
        SyncHttpClient.make_request.assert_called_once_with(
            SegmentDefinitionMicroClient._endpoint['get_keys'],
            environmentId='test_env_id',
            segmentName='test_segment',
            offset=0
        )
        
        # Verify the result matches the expected count
        assert result == 5

    def test_get_segment_from_sdk_endpoint(self, mocker):
        # Create mock HTTP client
        sc = SyncHttpClient('abc', 'abc')
        env = Environment(
            {
                'id': '123',
                'name': 'env1',
                'production':None,
                'creationTime' : None,
                'dataExportPermissions' : None,
                'environmentType' : None,
                'workspaceIds' : None,
                'changePermissions' : None,
                'type': None,
                'orgId' : None,
                'status' : None
            },
            mocker.Mock()
        )
        env.sdkApiToken = "sdkapixxxxsdkapixxxxsdkapixxxx123456"
        
        # Create segment definition with mock client
        seg = SegmentDefinitionMicroClient(sc)

        self.count = 0
        def fetch_segment_api(*_):
            self.count += 1
            if self.count == 1:
                return {"name": "test_segment", "since": -1, "till": 123, "added": ["key1", "key2"], "removed": []}

            if self.count == 2:
                return {"name": "test_segment", "since": 123, "till": 223, "added": ["key4", "key5"], "removed": ["key1"]}
            
            return {"name": "test_segment", "since": 223, "till": 223, "added": [], "removed": []}
            
        seg._fetch_segment_api = fetch_segment_api
        assert seg.get_all_keys("test_segment", env) == {"keys": {"key2", "key4", "key5"}, "count": 3}
        
        assert seg._build_basic_headers({"extra": "val"}) == {
            'Content-Type': 'application/json',
            'Authorization': "Bearer sdkapixxxxsdkapixxxxsdkapixxxx123456",
            'extra': 'val'
        }

    def test_errors_fetching_segment_keys(self, mocker):
        # Create mock HTTP client
        sc = SyncHttpClient('abc', 'abc')
        env = Environment(
            {
                'id': '123',
                'name': 'env1',
                'production':None,
                'creationTime' : None,
                'dataExportPermissions' : None,
                'environmentType' : None,
                'workspaceIds' : None,
                'changePermissions' : None,
                'type': None,
                'orgId' : None,
                'status' : None
            },
            mocker.Mock()
        )
        env.sdkApiToken = "sdkapixxxxsdkapixxxxsdkapixxxx123456"
        
        # Create segment definition with mock client
        seg = SegmentDefinitionMicroClient(sc)

        assert seg.get_all_keys("test_segment", env) == None

        def fetch_segment_api(*_):
            return None

        seg._fetch_segment_api = fetch_segment_api
        assert seg.get_all_keys("test_segment", env) == None

        env.sdkApiToken = None
        seg._fetch_segment_api = fetch_segment_api
        assert seg.get_all_keys("test_segment", env) == None

        env.sdkApiToken = "1234"
        seg._fetch_segment_api = fetch_segment_api
        assert seg.get_all_keys("test_segment", env) == None

        env.sdkApiToken = 1234
        seg._fetch_segment_api = fetch_segment_api
        assert seg.get_all_keys("test_segment", env) == None

    def test_errors_from_sdk_endpoint(self, mocker):
        # Create mock HTTP client
        sc = SyncHttpClient('abc', 'abc')
        env = Environment(
            {
                'id': '123',
                'name': 'env1',
                'production':None,
                'creationTime' : None,
                'dataExportPermissions' : None,
                'environmentType' : None,
                'workspaceIds' : None,
                'changePermissions' : None,
                'type': None,
                'orgId' : None,
                'status' : None
            },
            mocker.Mock()
        )
        env.sdkApiToken = "sdkapi"
        seg = SegmentDefinitionMicroClient(sc)

        response_mock = mocker.Mock()
        response_mock.status_code = 404
        response_mock.headers = {}
        response_mock.text = 'ok'
        get_mock = mocker.Mock()
        get_mock.return_value = response_mock
        mocker.patch('requests.get', new=get_mock)
        assert seg.get_all_keys("test_segment", env) == None
        
        response_mock = mocker.Mock()
        response_mock.status_code = 400
        response_mock.headers = {}
        response_mock.text = 'ok'
        get_mock = mocker.Mock()
        get_mock.return_value = response_mock
        mocker.patch('requests.get', new=get_mock)
        assert seg.get_all_keys("test_segment", env) == None
