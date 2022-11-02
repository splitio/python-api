from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import SplitDefinition
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client
from splitapiclient.microclients import SplitDefinitionMicroClient
from splitapiclient.microclients import ChangeRequestMicroClient

class TestSplitDefinition:
    '''
    Tests for the SplitDefinition class' methods
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
        sp = SplitDefinition({
            'name': 'split1',
            'treatments': [],
            'defaultTreatment': None,
            'baselineTreatment': None,
            'trafficAllocation': None,
            'rules': [],
            'defaultRule': [],
            'creationTime' : None,
            'lastUpdateTime' : None
        },
            'env_id',
            'ws_id',
            client
        )
        from splitapiclient.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(sp, 'split1', client)

    def test_getters_and_setters(self):
        '''
        '''
        sp = SplitDefinition({
            'name': 'split1',
            'environment': None,
            'trafficType' : None,
            'treatments': [],
            'defaultTreatment': None,
            'baselineTreatment': None,
            'trafficAllocation': None,
            'rules': [],
            'defaultRule': [],
            'creationTime' : None,
            'lastUpdateTime' : None
        })
        assert sp.name == 'split1'

    def test_update_definition(self, mocker):
        '''
        '''
        data = {
            'trafficType' : None,
            'treatments': [],
            'defaultTreatment': None,
            'baselineTreatment': None,
            'trafficAllocation': None,
            'rules': [],
            'defaultRule': [],
        }

        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        sp1 = SplitDefinition({
            'name': 'split1',
            'treatments': [],
            'defaultTreatment': None,
            'baselineTreatment': None,
            'trafficAllocation': None,
            'rules': [],
            'defaultRule': [],
        },
            'env_id',
            'ws_id',
            http_client_mock
        )
        attr = sp1.update_definition(data)

        http_client_mock.make_request.assert_called_once_with(
            SplitDefinitionMicroClient._endpoint['update_definition'],
            splitName = 'split1',
            workspaceId = 'ws_id',
            environmentId = 'env_id',
            body = data
        )
        data = {
            'name': None,
            'environment': None,
            'killed': None,
            'trafficType' : None,
            'treatments': None,
            'defaultTreatment': None,
            'baselineTreatment': None,
            'trafficAllocation': None,
            'rules': None,
            'defaultRule': None,
            'creationTime' : None,
            'lastUpdateTime' : None,
            'lastTrafficReceivedAt': None
        }
        assert attr.to_dict() == data

    def test_kill(self, mocker):
        '''
        '''
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        sp1 = SplitDefinition({
            'name': 'split1',
            'treatments': [],
            'defaultTreatment': None,
            'baselineTreatment': None,
            'trafficAllocation': None,
            'rules': [],
            'defaultRule': [],
        },
            'env_id',
            'ws_id',
            http_client_mock
        )
        attr = sp1.kill()

        http_client_mock.make_request.assert_called_once_with(
            SplitDefinitionMicroClient._endpoint['kill'],
            splitName = 'split1',
            workspaceId = 'ws_id',
            environmentId = 'env_id'
        )
        assert attr == True

    def test_restore(self, mocker):
        '''
        '''
        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = True
        sp1 = SplitDefinition({
            'name': 'split1',
            'treatments': [],
            'defaultTreatment': None,
            'baselineTreatment': None,
            'trafficAllocation': None,
            'rules': [],
            'defaultRule': [],
        },
            'env_id',
            'ws_id',
            http_client_mock
        )
        attr = sp1.restore()

        http_client_mock.make_request.assert_called_once_with(
            SplitDefinitionMicroClient._endpoint['restore'],
            splitName = 'split1',
            workspaceId = 'ws_id',
            environmentId = 'env_id'
        )
        assert attr == True

    def test_submit_change_request(self, mocker):
        '''
        '''
        data = {
            'split': {
                'name': 'split1',
                'treatments': [],
                'defaultTreatment': None,
                'baselineTreatment': None,
                'rules': [],
                'defaultRule': [],
            },
            'title': 'title',
            'operationType': 'op',
            'comment': 'com',
            'approvers': ['approver'],
        }

        http_client_mock = mocker.Mock(spec=BaseHttpClient)
        http_client_mock.make_request.return_value = data
        sp1 = SplitDefinition({
            'name': 'split1',
            'treatments': [],
            'defaultTreatment': None,
            'trafficAllocation': None,
            'rules': [],
            'defaultRule': [],
        },
            'env_id',
            'ws_id',
            http_client_mock
        )
        definition = {
            'environment': {},
            'trafficType' : {},
            'killed': None,
            'treatments': [],
            'defaultTreatment': None,
            'baselineTreatment': None,
            'trafficAllocation': None,
            'rules': [],
            'defaultRule': [],
            'openChangeRequestId' : None,
            'rolloutStatus': {'id': None}
        }

        attr = sp1.submit_change_request(definition, 'op', 'title', 'com', ['approver'], None)

        http_client_mock.make_request.assert_called_once_with(
            ChangeRequestMicroClient._endpoint['submit_change_request'],
            workspaceId = 'ws_id',
            environmentId = 'env_id',
            body = data
        )
        data = {
            'split': None,
            'segment': None,
            'id': None,
            'status': None,
            'title': None,
            'comment': None,
            'approvers': None,
            'operationType': None,
            'comments': None,
            'rolloutStatus': None
        }

        assert attr.to_dict() == data
