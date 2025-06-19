from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import RuleBasedSegmentDefinitionMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestRuleBasedSegmentDefinitionMicroClient:

    def test_list_single_page(self, mocker):
        '''
        Test listing rule-based segment definitions
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rbsd_mc = RuleBasedSegmentDefinitionMicroClient(sc)

        # Mock response with objects
        response = [{
                'name': 'rule_seg1',
                'trafficType': {'id': 'tt_123', 'name': 'user'},
                'creationTime': 1234567890,
            }, {
                'name': 'rule_seg2',
                'trafficType': {'id': 'tt_123', 'name': 'user'},
                'creationTime': 1234567891,
            }]
        
        # Set up the make_request mock
        SyncHttpClient.make_request.return_value = response
        
        result = rbsd_mc.list('env_123', 'ws_id')
        
        # Should be called once with default pagination parameters
        assert SyncHttpClient.make_request.call_count == 1
        SyncHttpClient.make_request.assert_called_once_with(
            RuleBasedSegmentDefinitionMicroClient._endpoint['all_items'],
            workspaceId='ws_id',
            environmentId='env_123',
            offset=0,
            limit=50
        )
        
        # Verify the first item in the result
        assert result[0].name == 'rule_seg1'
        assert result[0].environment['id'] == 'env_123'
        assert result[0].traffic_type.name == 'user'
        assert result[0].creation_time == 1234567890

        # Verify the second item in the result
        assert result[1].name == 'rule_seg2'
        assert result[1].environment['id'] == 'env_123'
        assert result[1].traffic_type.name == 'user'
        assert result[1].creation_time == 1234567891

    def test_find(self, mocker):
        '''
        Test finding a rule-based segment definition by name
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rbsd_mc = RuleBasedSegmentDefinitionMicroClient(sc)

        # Mock response containing the target segment
        first_page_response = [{
                'name': 'rule_seg1',
                'trafficType': {'id': 'tt_123', 'name': 'user'},
                'creationTime': 1234567890,
            }, {
                'name': 'rule_seg2',
                'trafficType': {'id': 'tt_123', 'name': 'user'},
                'creationTime': 1234567891,
            }]
        
        # Set up the make_request mock
        SyncHttpClient.make_request.return_value = first_page_response
        
        result = rbsd_mc.find('rule_seg2', 'env_123', 'ws_id')
        
        # Will make at least one request
        assert SyncHttpClient.make_request.call_count >= 1
        
        # First call should request with pagination parameters
        SyncHttpClient.make_request.assert_called_with(
            RuleBasedSegmentDefinitionMicroClient._endpoint['all_items'],
            workspaceId='ws_id',
            environmentId='env_123',
            offset=0,
            limit=50
        )
        
        # Verify the result
        assert result.name == 'rule_seg2'
        assert result.environment['id'] == 'env_123'
        assert result.traffic_type.name == 'user'
        assert result.creation_time == 1234567891
        
    def test_find_not_found(self, mocker):
        '''
        Test finding a rule-based segment definition by name when it doesn't exist
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rbsd_mc = RuleBasedSegmentDefinitionMicroClient(sc)

        # Empty response to simulate no matching segments
        empty_response = []
        
        # Set up the make_request mock
        SyncHttpClient.make_request.return_value = empty_response
        
        result = rbsd_mc.find('rule_seg_nonexistent', 'env_123', 'ws_id')
        
        # Will make at least one request
        assert SyncHttpClient.make_request.call_count >= 1
        
        # Result should be None since segment wasn't found
        assert result is None

    def test_update(self, mocker):
        '''
        Test updating a rule-based segment definition
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rbsd_mc = RuleBasedSegmentDefinitionMicroClient(sc)
        
        update_data = {
            'rules': [
                {
                    'condition': {
                        'combiner': 'AND',
                        'matchers': [
                            {
                                'type': 'EQUAL_TO',
                                'attribute': 'age',
                                'number': 40
                            }
                        ]
                    }
                }
            ]
        }
        
        response_data = {
            'name': 'rule_seg1',
            'environment': {'id': 'env_123', 'name': 'Production'},
            'trafficType': {'id': 'tt_123', 'name': 'user'},
            'creationTime': 1234567890,
            'rules': update_data['rules']
        }
        
        SyncHttpClient.make_request.return_value = response_data
        result = rbsd_mc.update('rule_seg1', 'env_123', 'ws_id', update_data)
        
        SyncHttpClient.make_request.assert_called_once_with(
            RuleBasedSegmentDefinitionMicroClient._endpoint['update'],
            body=update_data,
            workspaceId='ws_id',
            environmentId='env_123',
            segmentName='rule_seg1'
        )
        
        # Verify the result
        assert result.name == 'rule_seg1'
        assert result.environment['id'] == 'env_123'
        assert result.traffic_type.name == 'user'
        assert result.creation_time == 1234567890
