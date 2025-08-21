from splitapiclient.resources import SegmentDefinition
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict
from splitapiclient.util.fetch_options import FetchOptions, Backoff, build_fetch
from splitapiclient.resources import Environment
from splitapiclient.resources import segments
from splitapiclient.util.logger import LOGGER

import requests
import json
import time

_ON_DEMAND_FETCH_BACKOFF_BASE = 10  # backoff base starting at 10 seconds
_ON_DEMAND_FETCH_BACKOFF_MAX_WAIT = 60  # don't sleep for more than 1 minute
_ON_DEMAND_FETCH_BACKOFF_MAX_RETRIES = 10
SDK_URL = 'https://sdk.split.io/api'

class SegmentDefinitionMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'segments/ws/{workspaceId}/environments/{environmentId}?limit=50&offset={offset}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'get_keys': {
            'method': 'GET',
            'url_template': 'segments/{environmentId}/{segmentName}/keys?limit=100&offset={offset}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'import_from_json': {
            'method': 'PUT',
            'url_template': 'segments/{environmentId}/{segmentName}/uploadKeys?replace={replaceKeys}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'remove_keys': {
            'method': 'PUT',
            'url_template': 'segments/{environmentId}/{segmentName}/removeKeys',
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
        offset_val = 0
        final_list = []
        while True:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                workspaceId = workspace_id,
                environmentId = environment_id,
                offset = offset_val
            )
            for item in response['objects']:
                final_list.append(as_dict(item))
            offset = int(response['offset'])
            totalCount = int(response['totalCount'])
            limit = int(response['limit'])
            if totalCount>(offset+limit):
                offset_val = offset_val + limit
                continue
            else:
                break
        segment_definition_list = []
        for item in final_list:
            item['environment'] = {'id':environment_id, 'name':''}
            segment_definition_list.append(SegmentDefinition(item, self._http_client))
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
        LOGGER.error("Segment Definition Name does not exist")
        return None

    def get_keys(self, segment_name, environment_id):
        '''
        Returns a list of Keys in Segment in environemnt objects.

        :returns: list of keys in Segment in environemnt objects
        :rtype: list(string)
        '''
        offset_val = 0
        final_list = []
        while True:
            response = self._http_client.make_request(
                self._endpoint['get_keys'],
                environmentId = environment_id,
                segmentName = segment_name,
                offset = offset_val
            )
            for item in response['keys']:
                final_list.append(as_dict(item))
            offset = int(response['offset'])
            totalCount = int(response['count'])
            limit = int(response['limit'])
            if totalCount>(offset+limit):
                offset_val = offset_val + limit
                continue
            else:
                break
        return [item["key"] for item in final_list]



    def get_key_count(self, segment_name, environment_id):
        '''
        Returns a count of keys

        :returns: count of keys in Segment in environemnt objects
        :rtype: integer
        '''

        response = self._http_client.make_request(
                self._endpoint['get_keys'],
                environmentId = environment_id,
                segmentName = segment_name,
                offset = 0
            )
           
        return int(response['count'])


    def import_keys_from_json(self, segment_name, environment_id, replace_keys, data):
        '''
        import keys from csv file into segment

        :param segment: segment name, environment id, replace boolean flag, json data
        
        :returns: True
        :rtype: boolean
        '''
        response = self._http_client.make_request(
            self._endpoint['import_from_json'],
            body=as_dict(data),
            environmentId = environment_id,
            segmentName = segment_name,
            replaceKeys = replace_keys
        )
        return True

    def remove_keys(self, segment_name, environment_id, data):
        '''
        remove keys from csv file into segment

        :param segment: segment name, environment id, json data
        
        :returns: True
        :rtype: boolean
        '''
        response = self._http_client.make_request(
            self._endpoint['remove_keys'],
            body=as_dict(data),
            environmentId = environment_id,
            segmentName = segment_name
        )
        return True


    def get_all_keys(self, segment_name, environment):
        '''
        Get list of keys in segment in environment

        :param data: None
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: string of keys instance
        :rtype: string
        '''
        if not self._validate_sdkapi_key(environment.sdkApiToken):
            return None

        self._name = segment_name
        self._sdk_api_key = environment.sdkApiToken
        self._segment_storage = None
        self._segment_change_number = None
        self._metadata =  {
            'SplitSDKVersion': 'python-3.6.0-wrapper',
        }
        self._backoff = Backoff(
                                _ON_DEMAND_FETCH_BACKOFF_BASE,
                                _ON_DEMAND_FETCH_BACKOFF_MAX_WAIT)
        
        if self._get_segment_from_sdk_endpoint(self._name):
            keys = self._segment_storage.keys
            self._segment_storage = None
            return {
                "keys": keys,
                "count": len(keys)
            }

        LOGGER.error("Failed to fetch segment %s keys", self._name)
        return None

    def _validate_sdkapi_key(self, sdkApiToken):
        if sdkApiToken == None:
            LOGGER.error("Environment object does not have the SDK Api Key set, please set it before calling this method.")
            return False

        if not isinstance(sdkApiToken, str):
            LOGGER.error("SDK Api Key must be a string, please use a string to set it before calling this method.")
            return False

        if len(sdkApiToken) != 36:
            LOGGER.error("SDK Api Key string is invalid, please set it before calling this method.")
            return False
        
        return True
        
    def _fetch_until(self, segment_name, fetch_options, till=None):
        """
        Hit endpoint, update storage and return when since==till.

        :param segment_name: Name of the segment to update.
        :type segment_name: str

        :param fetch_options Fetch options for getting segment definitions.
        :type fetch_options splitio.api.FetchOptions

        :param till: Passed till from Streaming.
        :type till: int

        :return: last change number
        :rtype: int
        """
        while True:  # Fetch until since==till
            change_number = self._segment_change_number
            if change_number is None:
                change_number = -1
            if till is not None and till < change_number:
                # the passed till is less than change_number, no need to perform updates
                return change_number

            try:
                segment_changes = self._fetch_segment_api(segment_name, change_number,
                                                          fetch_options)
                if segment_changes == None:
                    return None
                
            except Exception as exc:
                LOGGER.debug('Exception raised while fetching segment %s', segment_name)
                LOGGER.error('Exception information: %s', str(exc))
                return None

            if change_number == -1:  # first time fetching the segment
                new_segment = segments.from_raw(segment_changes)
                self._segment_storage = new_segment
                self._segment_change_number = new_segment.change_number
            else:
                self._segment_change_number = segment_changes['till']
                self._segment_storage.keys.update(segment_changes['added'])
                [self._segment_storage.keys.remove(key) for key in  segment_changes['removed']]

            if segment_changes['till'] == segment_changes['since']:
                return segment_changes['till']

    def _attempt_segment_sync(self, segment_name, fetch_options, till=None):
        """
        Hit endpoint, update storage and return True if sync is complete.

        :param segment_name: Name of the segment to update.
        :type segment_name: str

        :param fetch_options Fetch options for getting feature flag definitions.
        :type fetch_options splitio.api.FetchOptions

        :param till: Passed till from Streaming.
        :type till: int

        :return: Flags to check if it should perform bypass or operation ended
        :rtype: bool, int, int
        """
        self._backoff.reset()
        remaining_attempts = _ON_DEMAND_FETCH_BACKOFF_MAX_RETRIES
        while True:
            remaining_attempts -= 1
            change_number = self._fetch_until(segment_name, fetch_options, till)
            if change_number == None:
                return False, 0, None
            
            if till is None or till <= change_number:
                return True, remaining_attempts, change_number

            elif remaining_attempts <= 0:
                return False, remaining_attempts, change_number

            how_long = self._backoff.get()
            time.sleep(how_long)

    def _get_segment_from_sdk_endpoint(self, segment_name, till=None):
        """
        Update a segment from queue

        :param segment_name: Name of the segment to update.
        :type segment_name: str

        :param till: ChangeNumber received.
        :type till: int

        :return: True if no error occurs. False otherwise.
        :rtype: bool
        """
        fetch_options = FetchOptions(True)  # Set Cache-Control to no-cache
        successful_sync, remaining_attempts, change_number = self._attempt_segment_sync(segment_name, fetch_options, till)
        if change_number == None:
            return False
        
        attempts = _ON_DEMAND_FETCH_BACKOFF_MAX_RETRIES - remaining_attempts
        if successful_sync:  # succedeed sync
            LOGGER.debug('Refresh completed in %d attempts.', attempts)
            return True
        with_cdn_bypass = FetchOptions(True, change_number)  # Set flag for bypassing CDN
        without_cdn_successful_sync, remaining_attempts, change_number = self._attempt_segment_sync(segment_name, with_cdn_bypass, till)
        if change_number == None:
            return False

        without_cdn_attempts = _ON_DEMAND_FETCH_BACKOFF_MAX_RETRIES - remaining_attempts
        if without_cdn_successful_sync:
            LOGGER.debug('Refresh completed bypassing the CDN in %d attempts.',
                          without_cdn_attempts)
            return True

        LOGGER.debug('No changes fetched after %d attempts with CDN bypassed.',
                        without_cdn_attempts)
        return False
    
    def _fetch_segment_api(self, segment_name, change_number, fetch_options):
        try:
            query, extra_headers = build_fetch(change_number, fetch_options, self._metadata)
            response = requests.get(
                SDK_URL + '/segmentChanges/{segment_name}'.format(segment_name=segment_name),
                headers=self._build_basic_headers(extra_headers),
                params=query,
            )
            if 200 <= response.status_code < 300:
                return json.loads(response.text)

            return None
        except Exception as exc:
            LOGGER.debug(
                'Error fetching %s because an exception was raised by the HTTPClient',
                segment_name)
            LOGGER.error(str(exc))
            return None
        
    def _build_basic_headers(self, extra_headers):
        """
        Build basic headers with auth.

        :param sdk_key: API token used to identify backend calls.
        :type sdk_key: str
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer %s" % self._sdk_api_key
        }
        if extra_headers is not None:
            headers.update(extra_headers)
        return headers