import subprocess
import time
import os
import os.path
from identify.main import get_client


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
        time.sleep(5)

    def test_successful_command_sequence(self):
        '''
        Test a basic command sequence using the get_client entry point function,
        issuing calls to a mocked API running in background.
        '''
        c = get_client({
            'base_url': 'http://localhost:8888',
            'apikey': 'Admin'
        })

        tts = c.get_traffic_types()
        assert isinstance(tts, list)

        envs = c.get_environments()
        assert isinstance(envs, list)

        attrs = c.get_attributes_for_traffic_type(tts[0].id)
        assert isinstance(attrs, list)

        new_attr = c.create_attribute_for_traffic_type(
            1,
            {
                'id': 'aa',
                'display_name': 'AA',
                'description': 'DESC',
                'data_type': 'STRING'
            }
        )
        assert isinstance(new_attr, object)

        attrs_2 = c.get_attributes_for_traffic_type(tts[0].id)
        assert isinstance(attrs_2, list)

        c.delete_attribute_from_schema(1, 'aa')
        attrs_3 = c.get_attributes_for_traffic_type(tts[0].id)
        assert isinstance(attrs_3, list)

        i1 = c.add_identity('1',  '1', 'keycita', {'a1': 'qwe'})
        assert isinstance(i1, object)

        i2 = c.update_identity('1',  '1', 'keycita', {'a1': 'qwe2'})
        assert isinstance(i2, object)

        i3 = c.patch_identity('1',  '1', 'keycita', {'a1': 'qwe3'})
        assert isinstance(i3, object)

        res_add_identities = c.add_identities(
            '1',
            '2',
            {
                'key1': {'a1': 'a', 'a2': 'b'},
                'key2': {'b1': 'c', 'c2': 'c'},
            }
        )
        assert res_add_identities is None

        res_delete_attr = c.delete_attributes_from_key('1',  '1', 'keycita')
        assert res_delete_attr is None

    def teardown_class(cls):
        '''
        Stop mock server
        '''
        cls.mock_server_subprocess.terminate()
