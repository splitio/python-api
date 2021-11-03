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
        self._creationTime = data.get('creationTime')
            
    @property
    def name(self):
        return self._name
            
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

