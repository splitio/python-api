from splitapiclient.resources import LargeSegment
from splitapiclient.resources import LargeSegmentDefinition
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.microclients import LargeSegmentMicroClient
import pytest

class TestLargeSegment:
    '''
    Tests for the LargeSegment class' methods
    '''
    @pytest.fixture
    def sample_data(self):
        '''Fixture providing sample segment data'''
        return {
            'name': 'segment1',
            'description': 'description1',
            'trafficType': {'id': '1', 'name': 'traffic1'},
            'workspaceId': 'workspace1',
            'creationTime': 1234567890,
            'tags': [{'name': 'tag1'}, {'name': 'tag2'}]
        }

        
    def test_constructor(self, sample_data):
        '''Test the constructor of LargeSegment'''
        segment = LargeSegment(sample_data, None)
        assert segment.name == 'segment1'
        assert segment.description == 'description1'
        assert segment.traffic_type.name == 'traffic1'
        assert segment.workspace_id == 'workspace1'
        assert segment.creation_time == 1234567890
        assert segment.tags == [{'name': 'tag1'}, {'name': 'tag2'}]

    def test_constructor_with_missing_fields(self):
        '''Test the constructor with partial or missing data'''
        partial_data = {
            'name': 'segment1',
            'description': 'description1'
            # Missing other fields
        }
        segment = LargeSegment(partial_data, None)
        assert segment.name == 'segment1'
        assert segment.description == 'description1'
        assert segment.traffic_type is None
        assert segment.workspace_id == None
        assert segment.creation_time == 0
        assert segment.tags == []

    def test_add_to_environment_success(self, mocker, sample_data):
        '''Test successful addition of segment to environment'''
        response_data = {
            'name': 'segment1',
            'id': 'seg_123',
            'environment': {
                'id': 'env_id',
                'name': 'environment1'
            },
            'trafficType': {
                'id': '1',
                'name': 'traffic1'
            },
            'creationTime': 1234567890,
            'workspaceId': 'workspace1'  
        }

        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        mock_microclient = mocker.Mock()



        # Mock the _http_client.make_request method to return response_data
        http_client_mock.make_request.return_value = response_data

        mocker.patch('splitapiclient.util.helpers.require_client', return_value=mock_microclient)

        segment = LargeSegment(response_data, http_client_mock)
        result = segment.add_to_environment('env_id')

        # Assertions

        assert result._name == 'segment1'
        assert result._id == 'seg_123'
        assert result._environment['id'] == 'env_id'
        assert result._environment['name'] == 'environment1'
        assert result._trafficType.id == '1'
        assert result._trafficType.name == 'traffic1'
        assert result._creationTime == 1234567890
        assert result._workspaceId == 'workspace1'
    
    def test_remove_from_environment_success(self, mocker):
        '''Test successful removal of segment from environment'''
        response_data = {
            'name': 'segment1',
            'id': 'seg_123',
            'environment': {
                'id': 'env_id',
                'name': 'environment1'
            },
            'trafficType': {
                'id': '1',
                'name': 'traffic1'
            },
            'creationTime': 1234567890,
            'workspaceId': 'workspace1'
        }

        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        mock_microclient = mocker.Mock()
        mock_microclient.remove_from_environment.return_value = True

        # Mock the _http_client.make_request method to return response_data
        http_client_mock.make_request.return_value = True

        mocker.patch('splitapiclient.util.helpers.require_client', return_value=mock_microclient)

        segment = LargeSegment(response_data, http_client_mock)
        result = segment.remove_from_environment('env_id')

        # Assertions
        assert result is True
        http_client_mock.make_request.assert_called_once_with({
            'method': 'DELETE',
            'url_template': 'large-segments/{environmentId}/{segmentName}',
            'headers': [{'name': 'Authorization', 'template': 'Bearer {value}', 'required': True}],
            'query_string': [],
            'response': True
        }, body='', segmentName='segment1', environmentId='env_id')
        #mock_microclient.remove_from_environment.assert_called_once_with('segment1', 'env_id')




    def test_empty_constructor(self):
        '''Test the constructor with no data'''
        segment = LargeSegment()
        assert segment.name is None
        assert segment.description is None
        assert segment.traffic_type is None
        assert segment.workspace_id is None
        assert segment.creation_time == 0
        assert segment.tags == []



