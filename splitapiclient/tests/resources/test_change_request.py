from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import ChangeRequest
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client
from splitapiclient.microclients import ChangeRequestMicroClient
import pytest

class TestChangeRequest:
    '''
    Tests for the ChangeRequest class' methods
    '''
    @pytest.fixture
    def sample_split_change_request(self):
        '''Fixture providing sample split change request data'''
        return {
            'id': 'cr123',
            'status': 'PENDING',
            'title': 'Update split configurations',
            'comment': 'Updating split to improve customer experience',
            'split': {
                'name': 'feature_toggle',
                'environment': {
                    'id': 'env_123',
                    'name': 'Production'
                }
            },
            'operationType': 'UPDATE',
            'approvers': ['user1@example.com', 'user2@example.com']
        }
        
    @pytest.fixture
    def sample_segment_change_request(self):
        '''Fixture providing sample segment change request data'''
        return {
            'id': 'cr124',
            'status': 'PENDING',
            'title': 'Update segment keys',
            'comment': 'Adding new users to the segment',
            'segment': {
                'name': 'premium_users',
                'keys': ['user1', 'user2', 'user3']
            },
            'operationType': 'UPDATE',
            'approvers': ['user1@example.com']
        }
        
    @pytest.fixture
    def sample_rule_based_segment_change_request(self):
        '''Fixture providing sample rule-based segment change request data'''
        return {
            'id': 'cr125',
            'status': 'PENDING',
            'title': 'Update rule-based segment rules',
            'comment': 'Changing user criteria',
            'ruleBasedSegment': {
                'name': 'advanced_users',
                'rules': [
                    {
                        'condition': {
                            'combiner': 'AND',
                            'matchers': [
                                {
                                    'type': 'GREATER_THAN_OR_EQUAL_TO',
                                    'attribute': 'age',
                                    'number': 25
                                }
                            ]
                        }
                    }
                ]
            },
            'operationType': 'UPDATE',
            'approvers': ['user1@example.com']
        }
    
    def test_constructor(self, mocker, sample_split_change_request):
        '''
        Test the constructor of ChangeRequest with split data
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'splitapiclient.resources.base_resource.BaseResource.__init__',
            new=mock_init
        )
        
        change_request = ChangeRequest(sample_split_change_request, client)
        
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(change_request, 'cr123', client)
        
        assert change_request._id == 'cr123'
        assert change_request._status == 'PENDING'
        assert change_request._title == 'Update split configurations'
        assert change_request._comment == 'Updating split to improve customer experience'
        assert change_request._split['name'] == 'feature_toggle'
        assert change_request._operationType == 'UPDATE'
        assert len(change_request._approvers) == 2
        assert 'user1@example.com' in change_request._approvers
        assert 'user2@example.com' in change_request._approvers

    def test_constructor_with_segment_data(self, sample_segment_change_request):
        '''
        Test the constructor of ChangeRequest with segment data
        '''
        change_request = ChangeRequest(sample_segment_change_request)
        
        assert change_request._id == 'cr124'
        assert change_request._status == 'PENDING'
        assert change_request._title == 'Update segment keys'
        assert change_request._comment == 'Adding new users to the segment'
        assert change_request._segment['name'] == 'premium_users'
        assert len(change_request._segment['keys']) == 3
        assert change_request._operationType == 'UPDATE'
        assert len(change_request._approvers) == 1
        assert change_request._approvers[0] == 'user1@example.com'

    def test_constructor_with_rule_based_segment_data(self, sample_rule_based_segment_change_request):
        '''
        Test the constructor of ChangeRequest with rule-based segment data
        '''
        change_request = ChangeRequest(sample_rule_based_segment_change_request)
        
        assert change_request._id == 'cr125'
        assert change_request._status == 'PENDING'
        assert change_request._title == 'Update rule-based segment rules'
        assert change_request._comment == 'Changing user criteria'
        assert change_request._operationType == 'UPDATE'
        
        # Note: Currently the change_request.py file doesn't have a field for ruleBasedSegment
        # This test assumes ruleBasedSegment is handled by the existing fields like ._segment
        # This might need to be updated if the ChangeRequest class is modified to specifically handle ruleBasedSegment

    def test_update_status(self, mocker, sample_split_change_request):
        '''
        Test updating the status of a change request
        '''
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        response_data = {
            'id': 'cr123',
            'status': 'APPROVED',
            'title': 'Update split configurations',
            'comment': 'Updating split to improve customer experience'
        }
        http_client_mock.make_request.return_value = response_data
        
        change_request = ChangeRequest(sample_split_change_request, http_client_mock)
        result = change_request.update_status('APPROVED', 'Looks good!')
        
        http_client_mock.make_request.assert_called_once_with(
            ChangeRequestMicroClient._endpoint['update_status'],
            changeRequestId='cr123',
            body={
                'status': 'APPROVED',
                'comment': 'Looks good!'
            }
        )
        
        assert result._id == 'cr123'
        assert result._status == 'APPROVED'
