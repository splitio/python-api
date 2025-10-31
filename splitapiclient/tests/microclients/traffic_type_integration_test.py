"""
Integration tests for TrafficTypeMicroClient and TrafficType resource.

These tests verify that TrafficType objects created by the microclient
can successfully use their instance methods that depend on stored state.
"""
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import TrafficTypeMicroClient, AttributeMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestTrafficTypeIntegration:
    """
    Integration tests between TrafficTypeMicroClient and TrafficType resource
    """

    def test_list_objects_can_fetch_attributes(self, mocker):
        """
        Verify that TrafficType objects from list() can call fetch_attributes()
        
        This is a regression test for a bug where list() didn't pass workspace_id,
        causing fetch_attributes() to fail with None workspace_id.
        """
        # Mock the HTTP client
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        ttmc = TrafficTypeMicroClient(sc)
        
        # Mock traffic type list response
        traffic_type_data = [{
            'id': '123',
            'name': 'user',
            'displayAttributeId': 'a1',
        }]
        
        # Mock attribute list response
        attribute_data = [{
            'id': 'attr1',
            'trafficTypeId': '123',
            'displayName': 'Email',
            'description': 'User email',
            'dataType': 'STRING',
            'isSearchable': True,
            'workspaceId': 'ws_id',
            'suggestedValues': []
        }]
        
        # Set up the mock to return different responses
        SyncHttpClient.make_request.side_effect = [
            traffic_type_data,  # First call: list traffic types
            attribute_data      # Second call: fetch attributes
        ]
        
        # Get traffic types via list()
        traffic_types = ttmc.list('ws_id')
        
        # Verify workspace_id was stored correctly
        assert traffic_types[0]._workspace_id == 'ws_id', \
            "TrafficType._workspace_id should be set by list()"
        
        # Now try to fetch attributes - this would fail if workspace_id is wrong
        attributes = traffic_types[0].fetch_attributes()
        
        # Verify the attribute fetch was called with correct parameters
        second_call = SyncHttpClient.make_request.call_args_list[1]
        assert second_call[1]['workspaceId'] == 'ws_id', \
            "fetch_attributes() should use the stored workspace_id"
        
        # Verify we got attributes back
        assert len(attributes) == 1
        assert attributes[0].display_name == 'Email'

    def test_list_objects_have_http_client(self, mocker):
        """
        Verify that TrafficType objects from list() have _client set
        
        This ensures objects can make API calls without passing apiclient parameter.
        """
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        ttmc = TrafficTypeMicroClient(sc)
        
        traffic_type_data = [{
            'id': '123',
            'name': 'user',
            'displayAttributeId': 'a1',
        }]
        
        SyncHttpClient.make_request.return_value = traffic_type_data
        
        traffic_types = ttmc.list('ws_id')
        
        # Verify http client was stored
        assert traffic_types[0]._client is not None, \
            "TrafficType._client should be set by list()"
        assert traffic_types[0]._client == sc, \
            "TrafficType._client should be the http_client"

    def test_find_object_can_fetch_attributes(self, mocker):
        """
        Verify that TrafficType objects from find() can call fetch_attributes()
        """
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        ttmc = TrafficTypeMicroClient(sc)
        
        traffic_type_data = [{
            'id': '123',
            'name': 'user',
            'displayAttributeId': 'a1',
        }]
        
        attribute_data = [{
            'id': 'attr1',
            'trafficTypeId': '123',
            'displayName': 'Email',
            'description': 'User email',
            'dataType': 'STRING',
            'isSearchable': True,
            'workspaceId': 'ws_id',
            'suggestedValues': []
        }]
        
        SyncHttpClient.make_request.side_effect = [
            traffic_type_data,  # First call: find traffic type
            attribute_data      # Second call: fetch attributes
        ]
        
        # Get traffic type via find()
        traffic_type = ttmc.find('user', 'ws_id')
        
        # Verify workspace_id was stored correctly
        assert traffic_type._workspace_id == 'ws_id', \
            "TrafficType._workspace_id should be set by find()"
        
        # Fetch attributes should work
        attributes = traffic_type.fetch_attributes()
        assert len(attributes) == 1

