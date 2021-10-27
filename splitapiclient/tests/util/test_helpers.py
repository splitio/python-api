from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.util.exceptions import InvalidArgumentException, \
    ClientRequiredError, InvalidModelException
from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.resources import Attribute, Environment, Identity, TrafficType, Workspace, Segment, Split, User, Group
from splitapiclient.main.apiclient import BaseApiClient
from splitapiclient.http_clients.base_client import BaseHttpClient
from splitapiclient.microclients.attribute_microclient import AttributeMicroClient
from splitapiclient.microclients.environment_microclient import EnvironmentMicroClient
from splitapiclient.microclients.identity_microclient import IdentityMicroClient
from splitapiclient.microclients.traffic_type_microclient import TrafficTypeMicroClient
from splitapiclient.microclients.workspace_microclient import WorkspaceMicroClient
from splitapiclient.microclients.segment_microclient import SegmentMicroClient
from splitapiclient.microclients.split_microclient import SplitMicroClient
from splitapiclient.microclients.user_microclient import UserMicroClient
from splitapiclient.microclients.group_microclient import GroupMicroClient
from splitapiclient.main.sync_apiclient import SyncApiClient
from splitapiclient.util import helpers
import pytest

class TestHelperFuntions:
    '''
    '''

    def test_require_client(self, mocker):
        '''
        '''
        httpclient = mocker.Mock(spec=BaseHttpClient)
        apiclient = SyncApiClient({'base_url': 'http://test', 'apikey': '123'})

        models = ['Attribute', 'Environment', 'Identity', 'TrafficType', 'Workspace', 'Segment', 'Split', 'User', 'Group']
        microclients = [
            AttributeMicroClient,
            EnvironmentMicroClient,
            IdentityMicroClient,
            TrafficTypeMicroClient,
            WorkspaceMicroClient,
            SegmentMicroClient,
            SplitMicroClient,
            UserMicroClient,
            GroupMicroClient
        ]
        # Test an exception is thrown if no client is passed
        for m in models:
            with pytest.raises(ClientRequiredError):
                helpers.require_client(m, None, None)

        # Test that an invalid model raises an exception
        with pytest.raises(InvalidModelException):
            helpers.require_client('invalidModel', None, None)

        # Test that passing httpClient and no apiclient works
        for i, m in enumerate(models):
            c = helpers.require_client(m, httpclient, None)
            assert isinstance(c, microclients[i])

        # Test that passing ApiClient and no httpclient works
        for i, m in enumerate(models):
            c = helpers.require_client(m, None, apiclient)
            assert isinstance(c, microclients[i])

        # Test that passing both clients works
        for i, m in enumerate(models):
            c = helpers.require_client(m, httpclient, apiclient)
            assert isinstance(c, microclients[i])

    def test_as_dict(self, mocker):
        '''
        '''
        model_instances = [
            Attribute(),
            Identity(),
            Environment(),
            TrafficType(),
            Workspace(),
            Segment(),
            Split(),
            User(),
            Group()
        ]

        # Test it works for all subclasses of BaseResource
        for instance in model_instances:
            assert isinstance(helpers.as_dict(instance), dict)

        # Test it works for dictionaries
        assert isinstance(helpers.as_dict(dict()), dict)

        # Test if fails for anything other thatn those 2 cases
        with pytest.raises(InvalidArgumentException):
            helpers.as_dict('a string')
