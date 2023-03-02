from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import Split
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client
from splitapiclient.microclients import SplitMicroClient

class TestSplit:
    '''
    Tests for the Split class' methods
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
        sp = Split(
            {
                'name': 'name',
                'description': '1',
            },
            'ws_id',
            client
        )
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(sp, 'name', client)

    def test_getters_and_setters(self):
        '''
        '''
        sp1 = Split(
            {
                'name': 'name',
                'description': '1',
            },
            'ws_id',
        )
        assert sp1.name == 'name'
        assert sp1.description == '1'

    def test_add_to_environment(self, mocker):
        '''
        '''
        data = {
            'name': 'split1',
            'environment': {},
            'trafficType' : {},
            'killed': None,
            'treatments': [],
            'defaultTreatment': None,
            'baselineTreatment': None,
            'trafficAllocation': None,
            'rules': [],
            'defaultRule': [],
            'creationTime' : None,
            'lastUpdateTime' : None
        }
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        sp1 = Split(
            {
                'name': 'split1',
                'description': '1',
            },
            'ws_id',
            http_client_mock
        )
        attr = sp1.add_to_environment('env_id', data)

        http_client_mock.make_request.assert_called_once_with(
            SplitMicroClient._endpoint['add_to_environment'],
            body = data,
            splitName = 'split1',
            workspaceId = 'ws_id',
            environmentId = 'env_id'
        )
        data = {
            'name': 'split1',
        }
        data['trafficType'] = None
        data['environment'] = None
        data['killed'] = None
        data['treatments'] = None
        data['defaultTreatment'] = None
        data['baselineTreatment'] = None
        data['trafficAllocation'] = None
        data['rules'] = None
        data['defaultRule'] = None
        data['creationTime'] = None
        data['lastUpdateTime'] = None
        data['lastTrafficReceivedAt'] = None
        
        assert attr.to_dict() == data

    def test_remove_from_environment(self, mocker):
        '''
        '''
        environment_id = 'e1'
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        sp = Split(
            {
                'name': 'name',
                'description': '1',
            },
            'ws_id',
            http_client_mock
        )
        title="title"
        comment="comment"
        attr = sp.remove_from_environment(environment_id, comment, title)

        http_client_mock.make_request.assert_called_once_with(
            SplitMicroClient._endpoint['remove_from_environment'],
            workspaceId = 'ws_id',
            splitName = 'name',
            environmentId = environment_id,
            title=title,
            comment=comment
        )
        assert attr == True

    def test_update_description(self, mocker):
        '''
        '''
        data = {
            'name': 'split1',
            'description': '2',
            'trafficType' : None,
            'creationTime' : None,
            'id': 'split1',
            'rolloutStatus': None,
            'rolloutStatusTimestamp': None,
            'tags': None,
            'owners': None
        }

        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        sp1 = Split(
            {
                'name': 'split1',
                'description': '1',
            },
            'ws_id',
            http_client_mock
        )
        attr = sp1.update_description('2')

        http_client_mock.make_request.assert_called_once_with(
            SplitMicroClient._endpoint['update_description'],
            splitName = 'split1',
            workspaceId = 'ws_id',
            body = '2'
        )
        assert attr.to_dict() == data

    def test_associate_tags(self, mocker):
        '''
        '''
        tags = ['tag1', 'tag2']
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        sp = Split(
            {
                'name': 'name',
                'description': '1',
            },
            'ws_id',
            http_client_mock
        )
        attr = sp.associate_tags(tags)

        http_client_mock.make_request.assert_called_once_with(
            SplitMicroClient._endpoint['associate_tags'],
            workspaceId = 'ws_id',
            splitName = 'name',
            body = tags
        )
        assert attr == True
