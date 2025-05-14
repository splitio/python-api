from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.microclients import RuleBasedSegmentMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestRuleBasedSegmentMicroClient:

    def test_list_single_page(self, mocker):
        '''
        Test listing rule-based segments (single page)
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rbs_mc = RuleBasedSegmentMicroClient(sc)
        
        # Response with objects
        response = [{
                'name': 'rule_seg1',
                'description': 'rule based segment description',
                'creationTime': 1234567890,
                'tags': [{'name': 'tag1'}]
            }, {
                'name': 'rule_seg2',
                'description': 'another rule based segment',
                'creationTime': 1234567891,
                'tags': [{'name': 'tag2'}]
            }]
        
        # Set up the make_request mock to return the response
        SyncHttpClient.make_request.return_value = response
        
        result = rbs_mc.list('ws_id')
        
        # Should be called once with pagination parameters
        assert SyncHttpClient.make_request.call_count >= 1
        SyncHttpClient.make_request.assert_called_with(
            RuleBasedSegmentMicroClient._endpoint['all_items'],
            workspaceId='ws_id',
            offset=0,
            limit=50
        )
        
        # Verify results by checking properties individually
        assert len(result) == 2
        
        # Check first segment
        assert result[0].name == 'rule_seg1'
        assert result[0].description == 'rule based segment description'
        assert result[0].creation_time == 1234567890
        assert len(result[0].tags) == 1
        assert result[0].tags[0]['name'] == 'tag1'
        
        # Check second segment
        assert result[1].name == 'rule_seg2'
        assert result[1].description == 'another rule based segment'
        assert result[1].creation_time == 1234567891
        assert len(result[1].tags) == 1
        assert result[1].tags[0]['name'] == 'tag2'

    def test_find(self, mocker):
        '''
        Test finding a rule-based segment by name
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rbs_mc = RuleBasedSegmentMicroClient(sc)
        
        # Response with objects including the target segment
        response = [{
                'name': 'rule_seg1',
                'description': 'rule based segment description',
                'creationTime': 1234567890,
                'tags': [{'name': 'tag1'}]
            }, {
                'name': 'rule_seg2',
                'description': 'another rule based segment',
                'creationTime': 1234567891,
                'tags': [{'name': 'tag2'}]
            }]
        
        # Set up the make_request mock
        SyncHttpClient.make_request.return_value = response
        
        result = rbs_mc.find('rule_seg2', 'ws_id')
        
        # Should make at least one request to get segments
        assert SyncHttpClient.make_request.call_count >= 1
        SyncHttpClient.make_request.assert_called_with(
            RuleBasedSegmentMicroClient._endpoint['all_items'],
            workspaceId='ws_id',
            offset=0,
            limit=50
        )
        
        # Verify the result by checking properties individually
        assert result is not None
        assert result.name == 'rule_seg2'
        assert result.description == 'another rule based segment'
        assert result.creation_time == 1234567891
        assert result.tags[0]['name'] == 'tag2'

    def test_add(self, mocker):
        '''
        Test adding a rule-based segment
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rbs_mc = RuleBasedSegmentMicroClient(sc)
        
        segment_data = {
            'name': 'new_rule_seg',
            'description': 'new rule based segment',
            'tags': [{'name': 'tag3'}]
        }
        
        response_data = {
            'name': 'new_rule_seg',
            'description': 'new rule based segment',
            'creationTime': 1234567892,
            'trafficType': {'id': 'tt_123', 'name': 'user'},
            'tags': [{'name': 'tag3'}]
        }

        SyncHttpClient.make_request.return_value = response_data
        result = rbs_mc.add(segment_data, 'user', 'ws_id')
        
        SyncHttpClient.make_request.assert_called_once_with(
            RuleBasedSegmentMicroClient._endpoint['create'],
            body=segment_data,
            workspaceId='ws_id',
            trafficTypeName='user'
        )
        
        # Test individual properties instead of the entire to_dict()
        assert result.name == 'new_rule_seg'
        assert result.description == 'new rule based segment'
        assert result.traffic_type is not None
        assert result.traffic_type.name == 'user'
        assert result.workspace_id == 'ws_id'
        assert result.creation_time == 1234567892
        assert len(result.tags) == 1
        assert result.tags[0]['name'] == 'tag3'

    def test_delete(self, mocker):
        '''
        Test deleting a rule-based segment
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rbs_mc = RuleBasedSegmentMicroClient(sc)
        
        response_data = {'success': True}
        SyncHttpClient.make_request.return_value = response_data
        
        result = rbs_mc.delete('rule_seg1', 'ws_id')
        
        SyncHttpClient.make_request.assert_called_once_with(
            RuleBasedSegmentMicroClient._endpoint['delete'],
            workspaceId='ws_id',
            segmentName='rule_seg1'
        )
        
        assert result == response_data

    def test_add_to_environment(self, mocker):
        '''
        Test adding a rule-based segment to environment
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rbs_mc = RuleBasedSegmentMicroClient(sc)
        
        response_data = {
            'name': 'rule_seg1',
            'environment': {'id': 'env_123', 'name': 'Production'},
            'trafficType': {'id': 'tt_123', 'name': 'user'}
        }
        
        SyncHttpClient.make_request.return_value = response_data
        result = rbs_mc.add_to_environment('rule_seg1', 'env_123')
        
        SyncHttpClient.make_request.assert_called_once_with(
            RuleBasedSegmentMicroClient._endpoint['add_to_environment'],
            body="",
            segmentName='rule_seg1',
            environmentId='env_123'
        )
        
        # Check individual properties
        assert result.name == 'rule_seg1'
        assert result.environment is not None
        assert result.environment['id'] == 'env_123'
        assert result.environment['name'] == 'Production'
        assert result.traffic_type is not None
        assert result.traffic_type.name == 'user'

    def test_remove_from_environment(self, mocker):
        '''
        Test removing a rule-based segment from an environment
        '''
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rbs_mc = RuleBasedSegmentMicroClient(sc)
        
        response_data = {'success': True}
        SyncHttpClient.make_request.return_value = response_data
        
        result = rbs_mc.remove_from_environment('rule_seg1', 'env_123')
        
        SyncHttpClient.make_request.assert_called_once_with(
            RuleBasedSegmentMicroClient._endpoint['remove_from_environment'],
            body='',
            segmentName='rule_seg1',
            environmentId='env_123'
        )
        
        assert result == response_data
