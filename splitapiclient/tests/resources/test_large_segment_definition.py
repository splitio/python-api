from splitapiclient.resources import LargeSegmentDefinition
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.microclients import LargeSegmentDefinitionMicroClient
import pytest

class TestLargeSegmentDefinition:
    '''
    Tests for the LargeSegmentDefinition class' methods
    '''
    def test_constructor(self):
        '''
        Test the constructor of LargeSegmentDefinition
        '''
        data = {
            'id': '1',
            'name': 'segment1',
            'environment': {'id': 'env1', 'name': 'environment1'},
            'trafficType': {'id': '1', 'name': 'traffic1'},
            'creationTime': 1234567890
        }
        segment_def = LargeSegmentDefinition(data)
        assert segment_def.id == '1'
        assert segment_def.name == 'segment1'
        assert segment_def.environment['id'] == 'env1'
        assert segment_def.traffic_type.name == 'traffic1'
        assert segment_def.creation_time == 1234567890

    def test_remove_all_members(self, mocker):
        '''
        Test the remove_all_members method of LargeSegmentDefinition
        '''
        data = {
            'id': '1',
            'name': 'segment1',
            'environment': {'id': 'env1', 'name': 'environment1'},
            'trafficType': {'id': '1', 'name': 'traffic1'},
            'creationTime': 1234567890,
            'workspaceId': 'workspace1'
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        segment_def = LargeSegmentDefinition(data, http_client_mock)

        attr = segment_def.remove_all_members( 'title', 'comment',['approver1'], 'workspace1')

        http_client_mock.make_request.assert_called_once_with(
            LargeSegmentDefinitionMicroClient._endpoint['make_cr'],
            body={
                'largeSegment': {'name': 'segment1'},
                'operationType': 'ARCHIVE',
                'title': 'title',
                'comment': 'comment',
                'approvers': ['approver1']
            },
            environmentId='env1',
            workspaceId='workspace1'
        )
        assert attr == True

    def test_submit_upload(self, mocker):
        '''
        Test the submit_upload method of LargeSegmentDefinition
        '''
        data = {
            'id': '1',
            'name': 'segment1',
            'environment': {'id': 'env1', 'name': 'environment1'},
            'trafficType': {'id': '1', 'name': 'traffic1'},
            'creationTime': 1234567890,
            'workspaceId': 'workspace1'
        }
        
        # Mock the HTTP client
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        
        # Create the upload URL response structure that will be used for both calls
        upload_url_response = {

            'method': 'PUT',
            'transactionMetadata': {
                'headers': {
                    'Host': ['example.com']
                },
                            'url': 'https://example.com/upload',
            }
        }
        
        # Have make_request always return the URL response structure
        http_client_mock.make_request.return_value = upload_url_response
        
        segment_def = LargeSegmentDefinition(data, http_client_mock)

        # Mock the file open operation
        mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='file content'))
        
        # Mock the requests.put call
        mock_requests_put = mocker.patch('requests.put')
        mock_requests_put.return_value = mocker.Mock(status_code=200)
        
        # Execute the test
        attr = segment_def.submit_upload( 'title', 'comment', ['approver1'], 'file_path')

        # Verify make_request was called with correct parameters
        assert len(http_client_mock.make_request.call_args_list) == 1
        first_call = http_client_mock.make_request.call_args
        assert first_call[1]['body'] == {
            'largeSegment': {'name': 'segment1'},
            'operationType': 'UPLOAD',
            'title': 'title',
            'comment': 'comment',
            'approvers': ['approver1']
        }
        assert first_call[1]['environmentId'] == 'env1'
        assert first_call[1]['workspaceId'] == 'workspace1'

        # Verify the file was opened
        mock_open.assert_called_once_with('file_path', 'rb')

        # Verify the requests.put call
        mock_requests_put.assert_called_once()
        args, kwargs = mock_requests_put.call_args
        assert args[0] == 'https://example.com/upload'
        assert kwargs['headers'] == {'Host': 'example.com'}

        # The final result should be the response from requests.put
        assert attr == mock_requests_put.return_value

    def test_properties(self):
        '''
        Test the properties of LargeSegmentDefinition
        '''
        data = {
            'id': '1',
            'name': 'segment1',
            'environment': {'id': 'env1', 'name': 'environment1'},
            'trafficType': {'id': '1', 'name': 'traffic1'},
            'creationTime': 1234567890
        }
        segment_def = LargeSegmentDefinition(data)
        assert segment_def.id == '1'
        assert segment_def.name == 'segment1'
        assert segment_def.environment['id'] == 'env1'
        assert segment_def.traffic_type.name == 'traffic1'
        assert segment_def.creation_time == 1234567890

    def test_empty_constructor(self):
        '''
        Test the constructor of LargeSegmentDefinition with empty data
        '''
        segment_def = LargeSegmentDefinition()
        assert segment_def.id is None
        assert segment_def.name is None
        assert segment_def.environment is None
        assert segment_def.traffic_type is None
        assert segment_def.creation_time is None