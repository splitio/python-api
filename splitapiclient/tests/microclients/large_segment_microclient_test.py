from splitapiclient.microclients import LargeSegmentDefinitionMicroClient
from splitapiclient.http_clients.base_client import BaseHttpClient
import pytest
import requests

class TestLargeSegmentDefinitionMicroClient:
    '''
    Tests for the LargeSegmentDefinitionMicroClient class' methods
    '''

    def test_remove_all_members(self, mocker):
        '''
        Test the remove_all_members method of LargeSegmentDefinitionMicroClient
        '''
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        client = LargeSegmentDefinitionMicroClient(http_client_mock)

        attr = client.remove_all_members('workspace1', 'env1', 'segment1', 'title', 'comment', ['approver1'])

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
        Test the submit_upload method of LargeSegmentDefinitionMicroClient
        '''
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = {
            'url': 'http://example.com/upload',
            'method': 'PUT',
            'transactionMetadata': {
                'headers': {
                    'Host': ['example.com']
                }
            }
        }
        client = LargeSegmentDefinitionMicroClient(http_client_mock)

        attr = client.submit_upload('workspace1', 'env1', 'segment1', 'title', 'comment', ['approver1'])

        http_client_mock.make_request.assert_called_once_with(
            LargeSegmentDefinitionMicroClient._endpoint['make_cr'],
            body={
                'largeSegment': {'name': 'segment1'},
                'operationType': 'UPLOAD',
                'title': 'title',
                'comment': 'comment',
                'approvers': ['approver1']
            },
            environmentId='env1',
            workspaceId='workspace1'
        )
        assert attr == http_client_mock.make_request.return_value

    def test_upload_file(self, mocker):
        '''
        Test the upload_file method of LargeSegmentDefinitionMicroClient
        '''
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        client = LargeSegmentDefinitionMicroClient(http_client_mock)

        file_path = 'path/to/file.csv'
        
        # Set up the mocks before the test
        mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='file content'))
        mock_requests_put = mocker.patch('requests.put', return_value=mocker.Mock(status_code=200))

        # Execute the test
        result = {

            'method': 'PUT',
            'transactionMetadata': {
                'headers': {
                    'Host': ['example.com']
                },
                            'url': 'http://example.com/upload',
            }
        }
        attr = client.upload_file(result, file_path)

        # Verify the mocks were called correctly
        mock_open.assert_called_once_with(file_path, 'rb')
        mock_requests_put.assert_called_once_with(
            'http://example.com/upload',
            headers={'Host': 'example.com'},
            data=mocker.ANY
        )
        assert attr == mock_requests_put.return_value