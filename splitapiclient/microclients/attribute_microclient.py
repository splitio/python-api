
from splitapiclient.resources import Attribute
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class AttributeMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'schema/ws/{workspaceId}/trafficTypes/{trafficTypeId}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'create': {
            'method': 'POST',
            'url_template': 'schema/ws/{workspaceId}/trafficTypes/{trafficTypeId}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'import_attributes_from_json': {
            'method': 'POST',
            'url_template': 'schema/ws/{workspaceId}/trafficTypes/{trafficTypeId}/attribute:bulk',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'delete': {
            'method': 'DELETE',
            'url_template': 'schema/ws/{workspaceId}/trafficTypes/{trafficTypeId}/{attributeId}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': False,
        },
    }

    def __init__(self, http_client):
        '''
        '''
        self._http_client = http_client

    def list(self, traffic_type_id, workspace_id):
        '''
        Returns a list of Attribute objects.

        :param traffic_type_id: Id of the TrafficType whose attributes will be
            returned
        :rtype: list(Attribute)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items'],
            trafficTypeId = traffic_type_id,
            workspaceId = workspace_id
        )
        final_array=[]
        for item in response:
            item['workspaceId'] = workspace_id
            final_array.append(Attribute(item))
        return final_array

    def find(self, attribute_id, traffic_type_name, workspace_id):
        '''
        Find Attribute in a TrafficType for a workspace

        :returns: Attribute object
        :rtype: Attribute
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items'],
            trafficTypeId = traffic_type_name,
            workspaceId = workspace_id
        )
        for item in response:
            if item['id']==attribute_id:
                item['workspaceId'] = workspace_id
                return Attribute(item, self._http_client)
        LOGGER.error("Attribute Id does not exist")
        return None

    def save(self, attribute):
        '''
        Create a new attribute.

        :param attribute: Attribute instance or dict with camelcase keys
            containing Attribute properties

        :returns: newly created attribute
        :rtype: Attribute
        '''
        wsId = attribute._workspace_id
        data = as_dict(attribute)
        del data['workspaceId']
        del data['isSearchable']
        response = self._http_client.make_request(
            self._endpoint['create'],
            data,
            trafficTypeId = data.get('trafficTypeId'),
            workspaceId = wsId
        )
        return Attribute(response, self._http_client)

    def delete(self, attribute_id, workspace_id, traffic_type_id):
        '''
        Delete an attribute by specifying its id and it's traffic type id.

        :param attribute_id: attribute's id
        :param traffic_type_id: atribute's traffic type id
        '''
        return self._http_client.make_request(
            self._endpoint['delete'],
            trafficTypeId=traffic_type_id,
            attributeId=attribute_id,
            workspaceId=workspace_id
        )

    def delete_by_instance(self, attribute):
        '''
        Delete an attribute

        :param attribute: Attribute instance
        '''
        data = as_dict(attribute)
        return self.delete(
            data.get('id'),
            attribute._workspace_id,
            data.get('trafficTypeId')
        )
    def import_attributes_from_json(self, workspaceId, trafficTypeId, data):
        '''
        import attributes from JSON file into Split

        :param segment: workspace id, traffic type id, json data
        
        :returns: bool
        '''
        res = self._http_client.make_request(
            self._endpoint['import_attributes_from_json'],
            body=data,
            workspaceId = workspaceId,
            trafficTypeId = trafficTypeId,
        )
        
        
        return True
