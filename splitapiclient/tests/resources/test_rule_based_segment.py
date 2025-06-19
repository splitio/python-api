from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import RuleBasedSegment
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client
from splitapiclient.microclients import RuleBasedSegmentMicroClient
import pytest

class TestRuleBasedSegment:
    '''
    Tests for the RuleBasedSegment class' methods
    '''
    @pytest.fixture
    def sample_data(self):
        '''Fixture providing sample rule-based segment data'''
        return {
            'name': 'rule_segment1',
            'description': 'description1',
            'trafficType': {'id': '1', 'name': 'traffic1'},
            'workspaceId': 'workspace1',
            'creationTime': 1234567890,
            'tags': [{'name': 'tag1'}, {'name': 'tag2'}]
        }
        
    def test_constructor(self, mocker, sample_data):
        '''
        Test the constructor of RuleBasedSegment
        '''
        client = object()
        
        # We're not mocking BaseResource.__init__ anymore because it's called multiple times
        # (once for RuleBasedSegment and once for TrafficType)
        seg = RuleBasedSegment(sample_data, client)
        
        # Instead, verify the properties are set correctly
        assert seg._name == 'rule_segment1'
        assert seg._description == 'description1'
        assert seg._trafficType.id == '1'
        assert seg._trafficType.name == 'traffic1'
        assert seg._workspace_id == 'workspace1'
        assert seg._creationTime == 1234567890
        assert seg._tags == [{'name': 'tag1'}, {'name': 'tag2'}]

    def test_constructor_with_missing_fields(self):
        '''Test the constructor with partial or missing data'''
        partial_data = {
            'name': 'rule_segment1',
            'description': 'description1'
            # Missing other fields
        }
        segment = RuleBasedSegment(partial_data, None)
        assert segment.name == 'rule_segment1'
        assert segment.description == 'description1'
        assert segment.traffic_type is None
        assert segment.workspace_id == None
        assert segment.creation_time == 0
        assert segment.tags == []

    def test_getters(self, sample_data):
        '''
        Test the getters of RuleBasedSegment
        '''
        seg = RuleBasedSegment(sample_data)
        assert seg.name == 'rule_segment1'
        assert seg.description == 'description1'
        assert seg.traffic_type.name == 'traffic1'
        assert seg.workspace_id == 'workspace1'
        assert seg.creation_time == 1234567890
        assert seg.tags == [{'name': 'tag1'}, {'name': 'tag2'}]

    def test_add_to_environment(self, mocker, sample_data):
        '''
        Test adding a rule-based segment to an environment
        '''
        environment_id = 'env1'
        response_data = {
            'name': 'rule_segment1',
            'environment': {
                'id': environment_id,
                'name': 'Production'
            },
            'trafficType': {
                'id': '1',
                'name': 'traffic1'
            }
        }
        
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = response_data
        seg = RuleBasedSegment(sample_data, http_client_mock)
        
        result = seg.add_to_environment(environment_id)

        http_client_mock.make_request.assert_called_once_with(
            RuleBasedSegmentMicroClient._endpoint['add_to_environment'],
            body="",
            segmentName='rule_segment1',
            environmentId=environment_id
        )
        
        assert result.name == 'rule_segment1'
        assert result.environment['id'] == environment_id
        assert result.traffic_type.name == 'traffic1'

    def test_remove_from_environment(self, mocker, sample_data):
        '''
        Test removing a rule-based segment from an environment
        '''
        environment_id = 'env1'
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        seg = RuleBasedSegment(sample_data, http_client_mock)
        
        result = seg.remove_from_environment(environment_id)

        http_client_mock.make_request.assert_called_once_with(
            RuleBasedSegmentMicroClient._endpoint['remove_from_environment'],
            body="",
            segmentName='rule_segment1',
            environmentId=environment_id
        )
        
        assert result is True
