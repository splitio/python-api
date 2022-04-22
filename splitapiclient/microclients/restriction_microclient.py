from splitapiclient.resources import Restriction
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class RestrictionMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'restrictions?limit=20&offset={offset}&resource_type={resourceType}&resource_id={resourceId}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'create': {
            'method': 'PUT',
            'url_template': 'restrictions',
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

    def list(self, resource_type, resource_id):
        '''
        Returns a list of restriction objects.
        :rtype: list(Restriction)
        '''
        offset_val = 0
        final_list = []
        while True:
            response = self._http_client.make_request(
                self._endpoint['all_items'],
                offset = offset_val,
                resourceType = resource_type,
                resourceId = resource_id
            )
            for item in response['objects']:
                final_list.append(item)
            offset = int(response['offset'])
            totalCount = int(response['totalCount'])
            limit = int(response['limit'])
            if totalCount>(offset+limit):
                offset_val = offset_val + limit
                continue
            else:
                break
        return [Restriction(item, self._http_client) for item in final_list]
        
    def add(self, resource_type, resource_id, restrictions_list):
        '''
        add a new restriction to existing object

        :param Resource Type: object type (workspace, environment, etc.)
        :returns: newly created restrictions
        :rtype: Restriction
        '''
        data = {"resource":{"id": resource_id, "type": resource_type}, "operations":{"view":True}, "resourcePermissions":{"view": restrictions_list}}
        
#        data = as_dict(final_body)
        response = self._http_client.make_request(
            self._endpoint['create'],
            body=data
        )
        return Restriction(response, self._http_client)
