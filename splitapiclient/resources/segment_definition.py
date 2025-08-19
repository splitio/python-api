from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict
from splitapiclient.util.fetch_options import FetchOptions, Backoff, build_fetch
from splitapiclient.resources import TrafficType
from splitapiclient.resources import Environment
from splitapiclient.resources import segments
from splitapiclient.util.logger import LOGGER

import requests
import json
import csv
import time

_ON_DEMAND_FETCH_BACKOFF_BASE = 10  # backoff base starting at 10 seconds
_ON_DEMAND_FETCH_BACKOFF_MAX_WAIT = 60  # don't sleep for more than 1 minute
_ON_DEMAND_FETCH_BACKOFF_MAX_RETRIES = 10
SDK_URL = 'https://sdk.split.io/api'

class SegmentDefinition(BaseResource):
    '''
    '''
    _schema = {
        'name': 'string',
        'environment': {
            'id': 'string',
            'name':'string'
        },
        'trafficType' : {
            'id': 'string',
            'name': 'string'
        },
        'creationTime' : 'number'
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        BaseResource.__init__(self, data.get('name'), client)
        self._name = data.get('name')
        self._environment = data.get('environment')
        self._trafficType = TrafficType(data.get('trafficType')) if 'trafficType' in data else {}
        self._creationTime = data.get('creationTime') if 'creationTime' in data else 0
            
    @property
    def name(self):
        return self._name

    @property
    def traffic_type(self):
        return None if self._trafficType == {} else self._trafficType
        
    @property
    def environment(self):
        return self._environment

    @property
    def tags(self):
        return self._tags

    @property
    def creation_time(self):
        return None if  self._creationTime==0 else self._creationTime

    def get_key_count(self, apiclient=None):
        '''
        Get the key count for this segment definition in this environment

        :returns: the key count for the segment definition
        :rtype: integer
        '''
        imc = require_client('SegmentDefinition', self._client, apiclient)
        return imc.get_key_count(self._name, self._environment['id'])


    def get_keys(self, apiclient=None):
        '''
        Get list of keys in segment in environment

        :param data: None
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: string of keys instance
        :rtype: string
        '''
        imc = require_client('SegmentDefinition', self._client, apiclient)
        return imc.get_keys(self._name, self._environment['id'])

    def export_keys_to_csv(self, csv_file_name, apiclient=None):
        '''
        Get list of keys in segment in environment

        :param data: None
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: True if successful
        :rtype: boolean
        '''
        imc = require_client('SegmentDefinition', self._client, apiclient)
        fields = ['key']
        with open(csv_file_name, mode='w') as keysFile:
            keysWriter = csv.writer(keysFile,  delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for key in imc.get_keys(self._name, self._environment['id']):
                keysWriter.writerow([key])
        return True

    def import_keys_from_json(self, replace_keys, json_data, apiclient=None):
        '''
        import keys from csv file into segment
        
        :param data: replace boolean flag, json data
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: True if successful
        :rtype: boolean
        '''
        imc = require_client('SegmentDefinition', self._client, apiclient)
        keys = json_data['keys']
        if(len(keys) > 10000):
            # Split keys into batches of 10,000
            key_batches = [keys[i:i + 10000] for i in range(0, len(keys), 10000)]
            success = True
            # Process each batch
            for key_batch in key_batches:
                # Make a copy of the json_data to avoid modifying the original
                batch_data = json_data.copy()
                batch_data['keys'] = key_batch
                # If any batch fails, mark the entire operation as failed
                batch_result = imc.import_keys_from_json(self._name, self._environment['id'], replace_keys, batch_data)
                if not batch_result:
                    success = False
            return success
        else:
            return imc.import_keys_from_json(self._name, self._environment['id'], replace_keys, json_data)

    def remove_keys(self, json_data, apiclient=None):
        '''
        remove keys from segment
        
        :param data: json data
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: True if successful
        :rtype: boolean
        '''
        imc = require_client('SegmentDefinition', self._client, apiclient)
        return imc.remove_keys(self._name, self._environment['id'], json_data)

    def submit_change_request(self, keys, operation_type, title, comment, approvers, rollout_status_id, workspace_id, apiclient=None):
        '''
        submit a change request for segment definition

        :param data: ChangeRequest
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: ChangeRequest object
        :rtype: ChangeRequest
        '''
        data = {
            'segment': {
                'name':self._name,
                'keys': keys,
            },
            'operationType': operation_type,
            'title': title,
            'comment': comment,
            'approvers': approvers,
        }
        if rollout_status_id is not None:
            data['rolloutStatus'] = {'id': rollout_status_id}
        imc = require_client('ChangeRequest', self._client, apiclient)
        return imc.submit_change_request(self._environment['id'], workspace_id, data)

    def get_keys_from_sdk_endpoint(self, sdk_api_key):
        '''
        Get list of keys in segment in environment

        :param data: None
        :param apiclient: If this instance wasn't returned by the client,
            the IdentifyClient instance should be passed in order to perform the
            http call

        :returns: string of keys instance
        :rtype: string
        '''
        self._sdk_api_key = sdk_api_key
        self._segment_storage = None
        self._segment_change_number = None
        self._metadata =  {
            'SplitSDKVersion': 'python-10.4.0',
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
            except Exception as exc:
                LOGGER.debug('Exception raised while fetching segment %s', segment_name)
                LOGGER.error('Exception information: %s', str(exc))
                raise exc

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
        attempts = _ON_DEMAND_FETCH_BACKOFF_MAX_RETRIES - remaining_attempts
        if successful_sync:  # succedeed sync
            LOGGER.debug('Refresh completed in %d attempts.', attempts)
            return True
        with_cdn_bypass = FetchOptions(True, change_number)  # Set flag for bypassing CDN
        without_cdn_successful_sync, remaining_attempts, change_number = self._attempt_segment_sync(segment_name, with_cdn_bypass, till)
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

            raise Exception(response.text, response.status_code)
        except requests.HTTPError as exc:
            LOGGER.debug(
                'Error fetching %s because an exception was raised by the HTTPClient',
                segment_name)
            LOGGER.error(str(exc))
            raise Exception('Segments not fetched properly.') from exc
        
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