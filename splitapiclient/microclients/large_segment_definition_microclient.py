from splitapiclient.resources import LargeSegmentDefinition
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict
import urllib
import requests

class LargeSegmentDefinitionMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'large-segments/ws/{workspaceId}/environments/{environmentId}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'make_cr': {
            'method': 'POST',
            'url_template': 'changeRequests/ws/{workspaceId}/environments/{environmentId}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },

    }

    def __init__(self, http_client):
        '''
        Constructor
        '''
        self._http_client = http_client

    def list(self, environment_id, workspace_id):
        '''
        Returns a list of Segment in environemnt objects.

        :returns: list of Segment in environemnt objects
        :rtype: list(SegmentDefinition)
        '''
        final_list = []
        response = self._http_client.make_request(
            self._endpoint['all_items'],
            workspaceId = workspace_id,
            environmentId = environment_id,
        )
        for item in response:
            final_list.append(as_dict(item))


        segment_definition_list = []
        for item in final_list:
            item['environment'] = {'id':environment_id, 'name':''}
            item['workspaceId'] = workspace_id
            segment_definition_list.append(LargeSegmentDefinition(item, self._http_client))
        return segment_definition_list

    def find(self, segment_name, environment_id, workspace_id):
        '''
        Find Segment in environment list objects.

        :returns: SegmentDefinition object
        :rtype: SegmentDefinition
        '''
        for item in self.list(environment_id, workspace_id):
            if item.name == segment_name:
                return item
        LOGGER.error("Large Segment Definition Name does not exist")
        return None



    def remove_all_members(self, workspace_id, environment_id, name, title, comment, approvers):
        '''
        remove all segment members

        :param data: json data
        :param workspace_id: workspace id
        :param environment_id: environment id
        
        
        :returns: True
        :rtype: boolean
        '''
        
        data = {
            'largeSegment': {
                'name': name
            },
            'operationType': 'ARCHIVE',
            'title': title,
            'comment': comment,
            'approvers': approvers
        }
        response = self._http_client.make_request(
            self._endpoint['make_cr'],
            body=as_dict(data),
            environmentId = environment_id,
            workspaceId = workspace_id
        )     
        return True


    def submit_upload(self, workspace_id, environment_id, name, title,comment,approvers):
        '''
        remove keys from csv file into segment

        :param segment: segment name, environment id, json data
        
        :returns: True
        :rtype: boolean
        '''
        data ={
            'largeSegment': {
                'name': name
            },
            'operationType': 'UPLOAD',
            'title': title,
            'comment': comment,
            'approvers': approvers,
        }
        response = self._http_client.make_request(
            self._endpoint['make_cr'],
            body=as_dict(data),
            environmentId = environment_id,
            workspaceId = workspace_id
        )
        return response


    def upload_file(self, result, file_path):
        '''
        Upload a file to the specified URL.

        :param result: dictionary containing 'url', 'method', and 'transactionMetadata'
        :param file_path: path to the file to be uploaded
        
        :returns: response from the server
        :rtype: requests.Response
        '''
        url = result['transactionMetadata']['url']
        headers = {
            'Host': result['transactionMetadata']['headers']['Host'][0]
        }
        with open(file_path, 'rb') as file:
            response = requests.put(url, headers=headers, data=file)
        return response