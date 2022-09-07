from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import TrafficType
from splitapiclient.resources import Identity
from splitapiclient.resources import Attribute
from splitapiclient.microclients import AttributeMicroClient
from splitapiclient.microclients import IdentityMicroClient
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client


class TestTrafficType:
    '''
    Tests for the TrafficType class' methods
    '''
    def test_constructor(self, mocker):
        '''
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'splitapiclient.resources.base_resource.BaseResource.__init__',
            new=mock_init
        )
        tt = TrafficType(
            {
                'id': '123',
                'name': 'name',
                'displayAttributeId': 'a1'
            },
            'ws_id',
            client
        )
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(tt, '123', client)

    def test_getters_and_setters(self):
        '''
        '''
        tt1 = TrafficType()
        tt1.id = 'a'
        tt1.name = 'b'
        tt1.display_attribute_id = 'c'

        assert tt1.id == 'a'
        assert tt1.name == 'b'
        assert tt1.display_attribute_id == 'c'

    def test_fetch_attributes(self, mocker):
        '''
        '''
        data = [{
            'id': 'a1',
            'trafficTypeId': '1',
            'displayName': 'dn1',
            'description': 'd1',
            'dataType': 'string',
            'isSearchable': False,
            'workspaceId': None
        }, {
            'id': 'a2',
            'trafficTypeId': '1',
            'displayName': 'dn2',
            'description': 'd1',
            'dataType': 'string',
            'isSearchable': False,
            'workspaceId': None
        }]
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        tt1 = TrafficType(
            {
                'id': '1',
                'displayAttributeId': 'asd',
                'name': 'n1',
            },
            'ws_id',
            http_client_mock
        )

        attrs = tt1.fetch_attributes()

        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['all_items'],
            trafficTypeId=data[0]['trafficTypeId'],
            workspaceId='ws_id'
        )
        data = [{
            'id': 'a1',
            'trafficTypeId': '1',
            'displayName': 'dn1',
            'description': 'd1',
            'dataType': 'string',
            'isSearchable': False,
            'workspaceId': None
        }, {
            'id': 'a2',
            'trafficTypeId': '1',
            'displayName': 'dn2',
            'description': 'd1',
            'dataType': 'string',
            'isSearchable': False,
            'workspaceId': None
        }]
        assert attrs[0].to_dict() == data[0]
        assert attrs[1].to_dict() == data[1]

        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = data
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        tt2 = TrafficType({
            'id': '1',
            'displayAttributeId': 'asd',
            'name': 'n2'
        },
        'ws_id',
        )
        attrs = tt2.fetch_attributes(ic)
        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['all_items'],
            trafficTypeId=data[0]['trafficTypeId'],
            workspaceId='ws_id'
        )
        data = [{
            'id': 'a1',
            'trafficTypeId': '1',
            'displayName': 'dn1',
            'description': 'd1',
            'dataType': 'string',
            'isSearchable': False,
            'workspaceId': None
        }, {
            'id': 'a2',
            'trafficTypeId': '1',
            'displayName': 'dn2',
            'description': 'd1',
            'dataType': 'string',
            'isSearchable': False,
            'workspaceId': None
        }]
        assert attrs[0].to_dict() == data[0]
        assert attrs[1].to_dict() == data[1]

    def test_add_attribute(self, mocker):
        '''
        '''
        data = {
            'id': 'a1',
            'trafficTypeId': '1',
            'displayName': 'dn1',
            'isSearchable': None,
            'dataType': 'string',
            'description': 'd1',
            'workspaceId': None
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        tt1 = TrafficType(
            {
                'id': '1',
                'displayAttributeId': 'asd',
                'name': 'n1',
            },
            'ws_id',
            http_client_mock
        )
        attrib_data = {'id': 'a1',
                'displayName': 'dn1',
                'description': 'd1',
                'dataType': 'string',
                'trafficTypeId': '1',
                'workspaceId': 'ws_id'
        }

        attr = tt1.add_attribute(attrib_data)
        data = {
            'id': 'a1',
            'trafficTypeId': '1',
            'displayName': 'dn1',
            'dataType': 'string',
            'description': 'd1',
        }

        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['create'],
            data,
            trafficTypeId = data['trafficTypeId'],
            workspaceId = 'ws_id'
        )
        
        data['workspaceId']=None
        data['isSearchable']=None
        assert attr.to_dict() == data

        # Test adding an attribute instance
        data = {
            'id': 'a1',
            'trafficTypeId': '1',
            'displayName': 'dn1',
            'dataType': 'string',
            'description': 'd1',
        }
        atinstance = Attribute(data)
        http_client_mock.reset_mock()
        attr = tt1.add_attribute(atinstance)
        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
            workspaceId=None
        )
        data['workspaceId']=None
        data['isSearchable']=None
        assert attr.to_dict() == atinstance.to_dict()

        tt2 = TrafficType({
            'id': '1',
            'displayAttributeId': 'asd',
            'name': 'n2'
        },
        'ws_id'
        )
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = data
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        attr = tt2.add_attribute(data, ic)
        data = {
            'id': 'a1',
            'trafficTypeId': '1',
            'displayName': 'dn1',
            'dataType': 'string',
            'description': 'd1',
        }

        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
            workspaceId=None
        )
        data['workspaceId']=None
        data['isSearchable']=None
        assert attr.to_dict() == data

    def test_add_identity(self, mocker):
        '''
        '''
        data = {
            'key': 'key1',
            'trafficTypeId': '1',
            'environmentId': '1',
            'values': {'a1': 'v1'},
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        tt1 = TrafficType(
            {
                'id': '1',
                'name': 'tt1',
                'displayAttributeId': '111',
            },
            'ws_id',
            http_client_mock
        )

        attr = tt1.add_identity(data)

        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
            environmentId=data['environmentId'],
            key=data['key']
        )
        assert attr.to_dict() == data

        # Test by passing an instance instead of dict data
        http_client_mock.reset_mock()
        idinstance = Identity(data)
        tt1.add_identity(idinstance)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            data,
            trafficTypeId=idinstance.traffic_type_id,
            environmentId=idinstance.environment_id,
            key=idinstance.key
        )
        assert attr.to_dict() == data


        tt2 = TrafficType(
            {
                'id': '1',
                'name': 'tt1',
                'displayAttributeId': '111',
            },
            'ws_id',
        )

        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = data
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        attr = tt2.add_identity(data, ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
            environmentId=data['environmentId'],
            key=data['key']
        )
        assert attr.to_dict() == data

    def test_add_identities(self, mocker):
        '''
        '''
        data = [{
            'key': 'key1',
            'trafficTypeId': '1',
            'environmentId': '1',
            'values': {'a1': 'v1'},
        }, {
            'key': 'key2',
            'trafficTypeId': '1',
            'environmentId': '1',
            'values': {'a2': 'v2'},
        }]

        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = {
            'objects': data,
            'failed': [],
            'metadata': {}
        }
        tt1 = TrafficType(
            {
                'id': '1',
                'name': 'tt1',
                'displayAttributeId': '111'
            },
            'ws_id',
            http_client_mock
        )

        res1 = tt1.add_identities(data)

        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            data,
            trafficTypeId=data[0]['trafficTypeId'],
            environmentId=data[0]['environmentId'],
        )
        assert [s.to_dict() for s in res1.successful] == data
        assert isinstance(res1.failed, list)
        assert isinstance(res1.metadata, dict)

        # Test by passing an instances as well as raw dict data
        http_client_mock.reset_mock()
        idinstances = [Identity(data[0]), data[1]]
        res2 = tt1.add_identities(idinstances)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            data,
            trafficTypeId=idinstances[0].traffic_type_id,
            environmentId=idinstances[0].environment_id,
        )
        assert [s.to_dict() for s in res2.successful] == data
        assert isinstance(res2.failed, list)
        assert isinstance(res2.metadata, dict)


        tt2 = TrafficType({
            'id': '1',
            'name': 'tt1',
            'displayAttributeId': '111'
            },
            'ws_id',
        )

        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = {
            'objects': data,
            'failed': [],
            'metadata': {}
        }
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        res3 = tt2.add_identities(data, ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            data,
            trafficTypeId=data[0]['trafficTypeId'],
            environmentId=data[0]['environmentId'],
        )
        assert [s.to_dict() for s in res3.successful] == data
        assert isinstance(res3.failed, list)
        assert isinstance(res3.metadata, dict)

    def test_import_JSON(self, mocker):
        '''
        '''
        data = {
            'id': 'a1',
            'trafficTypeId': '1',
            'displayName': 'dn1',
            'isSearchable': None,
            'dataType': 'string',
            'description': 'd1',
            'workspaceId': 'ws_id'
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        tt1 = TrafficType(
            {
                'id': '1',
                'displayAttributeId': 'asd',
                'name': 'n1',
            },
            'ws_id',
            http_client_mock
        )
        attrib_data = [ {
                            "id": "anAttribute2",
                            "displayName": "An Attribute2",
                            "description": "my description here",
                            "dataType": "string",
                            "suggestedValues": [
                                "suggested",
                                "values"
                            ]
                        } ]


        tt1.import_attributes_from_json(attrib_data)


        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['import_attributes_from_json'],
            body=attrib_data,
            workspaceId = data['workspaceId'],
            trafficTypeId = data['trafficTypeId']
            
        )


