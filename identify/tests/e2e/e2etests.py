from __future__ import absolute_import, division, print_function, \
    unicode_literals
import subprocess
import time
import os
import os.path
from identify.main import get_client
from identify.resources.traffic_type import TrafficType
from identify.resources.environment import Environment
from identify.resources.attribute import Attribute
from identify.resources.identity import Identity


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
            'log_level': 'debug'
        })

        tts = c.get_traffic_types()
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
            'log_level': 'debug'
        })

        envs = c.get_environments()
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
            'log_level': 'debug'
        })

        attrs = c.get_attributes_for_traffic_type('1')
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
        new_attr = c.create_attribute_for_traffic_type(
            '1',
            {
                'id': 'aa',
                'displayName': 'AA',
                'description': 'DESC',
                'dataType': 'STRING',
                'isSearchable': False,
            }
        )
        assert new_attr_props == new_attr.to_dict()

        res_delete = c.delete_attribute_from_schema(1, 'aa')
        assert res_delete is None

    def test_identity_endpoints(self):
        '''
        '''
        c = get_client({
            'base_url': 'http://localhost:8888',
            'apikey': 'Admin',
            'log_level': 'debug'
        })

        i1 = c.add_identity('1',  '1', 'keycita', {'a1': 'qwe'})
        assert isinstance(i1, Identity)
        assert {
            'key': i1.key,
            'environmentId': i1.environment_id,
            'trafficTypeId': i1.traffic_type_id,
            'values': i1.values,
            'organizationId': i1.organization_id,
        } == i1.to_dict()

        i2 = c.update_identity('1',  '1', 'keycita', {'a1': 'qwe2'})
        assert isinstance(i2, Identity)
        assert {
            'key': i2.key,
            'environmentId': i2.environment_id,
            'trafficTypeId': i2.traffic_type_id,
            'values': i2.values,
            'organizationId': i2.organization_id,
        } == i2.to_dict()

        i3 = c.patch_identity('1',  '1', 'keycita', {'a1': 'qwe3'})
        assert isinstance(i3, Identity)
        assert {
            'key': i3.key,
            'environmentId': i3.environment_id,
            'trafficTypeId': i3.traffic_type_id,
            'values': i3.values,
            'organizationId': i3.organization_id,
        } == i3.to_dict()

        res_add_identities = c.add_identities(
            '1',
            '2',
            {
                'key1': {'a1': 'a', 'a2': 'b'},
                'key2': {'b1': 'c', 'c2': 'c'},
            },
            'oo1'
        )
        assert isinstance(res_add_identities, tuple)
        objs, failed = res_add_identities
        assert all(isinstance(i, Identity) for i in objs)
        assert all(isinstance(i['object'], Identity) for i in failed)
        assert all(
            {
                'key': i.key,
                'trafficTypeId': i.traffic_type_id,
                'environmentId': i.environment_id,
                'values': i.values,
                'organizationId': i.organization_id,
            } == i.to_dict()
            for i in objs
        )

        res_delete_attr = c.delete_attributes_from_key('1',  '1', 'keycita')
        assert res_delete_attr is None

    def teardown_class(cls):
        '''
        Stop mock server
        '''
        cls.mock_server_subprocess.terminate()
