from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.resources import SplitDefinition
from splitapiclient.http_clients.sync_client import SyncHttpClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.main import get_client
from splitapiclient.microclients import SplitDefinitionMicroClient
from splitapiclient.microclients import ChangeRequestMicroClient
def object_to_stringified_dict(obj):
    """
    Recursively converts an object and its nested objects to a stringified dictionary.
    Assumes that the object has a 'to_dict()' method for serialization.
    
    Args:
        obj: The object to be converted to a stringified dictionary.
        
    Returns:
        A stringified dictionary representation of the object.
    """
    if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
        return object_to_stringified_dict(obj.to_dict())  # Recursively call to_dict()
    elif isinstance(obj, dict):
        return {key: object_to_stringified_dict(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [object_to_stringified_dict(item) for item in obj]
    else:
        return obj  # For non-dict, non-list, and non-object types, return as is
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
            'killed': False,
            'trafficType' : {'displayAttributeId': None, 'id': None, 'name': None},
            'treatments': None,
            'defaultTreatment': None,
            'baselineTreatment': None,
            'trafficAllocation': None,
            'rules': None,
            'defaultRule': None,
            'creationTime' : None,
            'lastUpdateTime' : None,
            'lastTrafficReceivedAt': None,
            'flagSets': None,
            'impressionsDisabled': False
        }
        assert object_to_stringified_dict(attr) == data

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
            'flagSets': [],
            'impressionsDisabled': False
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
            'largeSegment': None,
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
