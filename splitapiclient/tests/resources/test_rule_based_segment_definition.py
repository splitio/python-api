from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.resources import RuleBasedSegmentDefinition
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client
from splitapiclient.microclients import RuleBasedSegmentDefinitionMicroClient
from splitapiclient.microclients import ChangeRequestMicroClient

class TestRuleBasedSegmentDefinition:
    '''
    Tests for the RuleBasedSegmentDefinition class' methods
    '''
    @pytest.fixture
    def sample_data(self):
        '''Fixture providing sample segment definition data'''
        return {
            'name': 'rule_segment1',
            'environment': {
                'id': 'env1',
                'name': 'Production'
            },
            'trafficType': {
                'id': '1',
                'name': 'traffic1'
            },
            'creationTime': 1234567890,
            'excludedKeys': ['key1', 'key2'],
            'excludedSegments': [
                {'name': 'segment1', 'type': 'whitelist'},
                {'name': 'segment2', 'type': 'whitelist'}
            ],
            'rules': [
                {
                    'condition': {
                        'combiner': 'AND',
                        'matchers': [
                            {
                                'type': 'EQUAL_TO',
                                'attribute': 'age',
                                'number': 30
                            }
                        ]
                    }
                }
            ]
        }
    
    def test_constructor(self, mocker, sample_data):
        '''
        Test the constructor of RuleBasedSegmentDefinition
        '''
        client = object()
        
        # We're not mocking BaseResource.__init__ anymore because it's called multiple times
        # (once for RuleBasedSegmentDefinition and once for TrafficType)
        seg = RuleBasedSegmentDefinition(sample_data, client)
        
        # Verify the properties are set correctly
        assert seg.name == 'rule_segment1'
        assert seg.environment['id'] == 'env1'
        assert seg.environment['name'] == 'Production'
        assert seg.traffic_type.name == 'traffic1'
        assert seg.creation_time == 1234567890
        assert len(seg.excluded_keys) == 2
        assert seg.excluded_keys[0] == 'key1'
        assert len(seg.excluded_segments) == 2
        assert seg.excluded_segments[0]['name'] == 'segment1'

    def test_getters(self, sample_data):
        '''
        Test the getters of RuleBasedSegmentDefinition
        '''
        seg = RuleBasedSegmentDefinition(sample_data)
        assert seg.name == 'rule_segment1'
        assert seg.environment['id'] == 'env1'
        assert seg.traffic_type.name == 'traffic1'
        assert seg.creation_time == 1234567890

    def test_update(self, mocker, sample_data):
        '''
        Test updating a rule-based segment definition
        '''
        update_data = {
            'rules': [
                {
                    'condition': {
                        'combiner': 'AND',
                        'matchers': [
                            {
                                'type': 'EQUAL_TO',
                                'attribute': 'age',
                                'number': 40  # Changed from 30 to 40
                            }
                        ]
                    }
                }
            ]
        }
        
        response_data = dict(sample_data)
        response_data['rules'] = update_data['rules']
        
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = response_data
        http_client_mock._workspace_id = 'workspace1'
        
        seg = RuleBasedSegmentDefinition(sample_data, http_client_mock, workspace_id=http_client_mock._workspace_id)
        result = seg.update(update_data)

        http_client_mock.make_request.assert_called_once_with(
            RuleBasedSegmentDefinitionMicroClient._endpoint['update'],
            body=update_data,
            workspaceId='workspace1',
            environmentId='env1',
            segmentName='rule_segment1'
        )
        
        assert result.name == 'rule_segment1'
        assert result.rules[0]['condition']['matchers'][0]['number'] == 40

    def test_submit_change_request(self, mocker, sample_data):
        '''
        Test submitting a change request for a rule-based segment definition
        '''
        rules = [
            {
                'condition': {
                    'combiner': 'AND',
                    'matchers': [
                        {
                            'type': 'EQUAL_TO',
                            'attribute': 'age',
                            'number': 25
                        }
                    ]
                }
            }
        ]
        
        operation_type = 'create'
        title = 'New Rule-Based Segment'
        comment = 'Adding a new rule'
        approvers = ['user1']
        rollout_status_id = None
        workspace_id = 'workspace1'
        
        expected_request = {
            'ruleBasedSegment': {
                'name': 'rule_segment1',
                'rules': rules,
                'excludedKeys': [],
                'excludedSegments': []
            },
            'operationType': operation_type,
            'title': title,
            'comment': comment,
            'approvers': approvers,
        }
        
        response_data = {
            'id': 'cr123',
            'status': 'PENDING',
            'title': title,
            'comment': comment,
            'approvers': approvers,
            'operationType': operation_type
        }
        
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = response_data
        
        seg = RuleBasedSegmentDefinition(sample_data, http_client_mock)
        result = seg.submit_change_request(
            rules, [], [], operation_type, title, comment, approvers, workspace_id
        )

        http_client_mock.make_request.assert_called_once_with(
            ChangeRequestMicroClient._endpoint['submit_change_request'],
            workspaceId=workspace_id,
            environmentId='env1',
            body=expected_request
        )
