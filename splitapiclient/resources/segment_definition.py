from __future__ import absolute_import, division, print_function, \
    unicode_literals
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.helpers import require_client, as_dict
from splitapiclient.resources import TrafficType
from splitapiclient.resources import Environment
import csv

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
            first_batch = True
            for key_batch in key_batches:
                # Make a copy of the json_data to avoid modifying the original
                batch_data = json_data.copy()
                batch_data['keys'] = key_batch
                # If any batch fails, mark the entire operation as failed
                # First batch uses original replace_keys value, subsequent batches use False
                batch_replace_keys = replace_keys if first_batch else False
                batch_result = imc.import_keys_from_json(self._name, self._environment['id'], batch_replace_keys, batch_data)
                if not batch_result:
                    success = False
                first_batch = False
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
