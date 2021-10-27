from __future__ import absolute_import, division, print_function, \
    unicode_literals
import subprocess
import time
import os
import os.path
from splitapiclient.main import get_client
from splitapiclient.resources.traffic_type import TrafficType
from splitapiclient.resources.environment import Environment
from splitapiclient.resources.workspace import Workspace
from splitapiclient.resources.attribute import Attribute
from splitapiclient.resources.identity import Identity
from splitapiclient.util.bulk_result import BulkOperationResult

class TestEndToEnd:
    '''
    '''
    def setup_class(cls):
        '''
        Start mock server
        '''
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cls.mock_server_subprocess = subprocess.Popen(
            ['python', os.path.join(dir_path, 'server.py')]
        )
        time.sleep(3)

    def test_traffic_type_endpoint(self):
        '''
        '''
        c = get_client({
            'base_url': 'http://localhost:8888',
            'apikey': 'Admin',
        })

        tts = c.traffic_types.list()
        assert isinstance(tts, list)
        assert all(isinstance(tt, TrafficType) for tt in tts)
        assert all(
            {
                'id': tt.id,
                'name': tt.name,
                'displayAttributeId': tt.display_attribute_id
            } == tt.to_dict()
            for tt in tts
        )

    def test_environments_endpoint(self):
        '''
        '''
        c = get_client({
            'base_url': 'http://localhost:8888',
            'apikey': 'Admin',
        })

        envs = c.environments.list()
        assert isinstance(envs, list)
        assert all(isinstance(env, Environment) for env in envs)
        assert all(
            {
                'id': env.id,
                'name': env.name,
            } == env.to_dict()
            for env in envs
        )

    def test_attribute_endpoints(self):
        '''
        '''
        c = get_client({
            'base_url': 'http://localhost:8888',
            'apikey': 'Admin',
        })

        attrs = c.attributes.list('1')
        assert isinstance(attrs, list)
        assert all(isinstance(attr, Attribute) for attr in attrs)
        assert all(
            {
                'id': attr.id,
                'trafficTypeId': attr.traffic_type_id,
                'displayName': attr.display_name,
                'description': attr.description,
                'dataType': attr.data_type,
                'isSearchable': attr.is_searchable
            } == attr.to_dict()
            for attr in attrs
        )

        new_attr_props = {
            'id': 'aa',
            'trafficTypeId': '1',
            'displayName': 'AA',
            'description': 'DESC',
            'dataType': 'STRING',
            'isSearchable': False,
        }
        new_attr = c.attributes.save(new_attr_props)
        assert new_attr_props == new_attr.to_dict()

        res_delete = c.attributes.delete_by_instance(new_attr)
        assert res_delete is None

    def test_identity_endpoints(self):
        '''
        '''
        c = get_client({
            'base_url': 'http://localhost:8888',
            'apikey': 'Admin',
        })

        data = {
            'key': 'key1',
            'environmentId': 'e1',
            'trafficTypeId': 'tt1',
            'values': {'a1': 'v1'},
            'organizationId': 'ooo1',
        }
        i1 = c.identities.save(data)
        assert isinstance(i1, Identity)
        assert data == i1.to_dict()

        data2 = {
            'key': 'key2',
            'environmentId': 'e2',
            'trafficTypeId': 'tt2',
            'values': {'a2': 'v2'},
            'organizationId': 'ooo2',
        }
        i2 = c.identities.update(data2)
        assert isinstance(i2, Identity)
        assert data2 == i2.to_dict()

        data3 = {
            'key': 'key3',
            'environmentId': 'e3',
            'trafficTypeId': 'tt3',
            'values': {'a3': 'v3'},
            'organizationId': 'ooo3',
        }
        i3 = c.identities.patch(data3)
        assert isinstance(i3, Identity)
        assert data3 == i3.to_dict()

        res_add_identities = c.identities.save_all([
            {
                'trafficTypeId': '1',
                'environmentId': '2',
                'key': 'key1',
                'values': {'a1': 'a', 'a2': 'b'},
                'organizationId': 'ooo1',
            },
            {
                'trafficTypeId': '1',
                'environmentId': '2',
                'key': 'key2',
                'values': {'b1': 'c', 'c2': 'c'},
                'organizationId': 'ooo1',
            },
        ])

        assert isinstance(res_add_identities, BulkOperationResult)
        assert all(
            isinstance(i, Identity)
            for i in res_add_identities.successful
        )
        assert all(isinstance(
            i['object'], Identity)
            for i in res_add_identities.failed
        )
        assert all(
            {
                'key': i.key,
                'trafficTypeId': i.traffic_type_id,
                'environmentId': i.environment_id,
                'values': i.values,
                'organizationId': i.organization_id,
            } == i.to_dict()
            for i in res_add_identities.successful
        )

        res_delete_attr = c.identities.delete(
            '1',  '1', 'keycita'
        )
        assert res_delete_attr is None

    def teardown_class(cls):
        '''
        Stop mock server
        '''
        cls.mock_server_subprocess.terminate()
