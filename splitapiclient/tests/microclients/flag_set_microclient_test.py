import pytest
from unittest.mock import MagicMock
from splitapiclient.microclients.flag_set_microclient import FlagSetMicroClient
from splitapiclient.resources.flag_set import FlagSet

class TestFlagSetMicroClient:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_http_client = MagicMock()
        self.client = FlagSetMicroClient(self.mock_http_client)

    def test_list(self):
        self.mock_http_client.make_request.side_effect = [
            {'data': [{'id': 1, 'name': 'flag1'}], 'nextMarker': None}
        ]
        result = self.client.list(workspace_id='workspace1')
        assert len(result) == 1
        assert isinstance(result[0], FlagSet)
        assert result[0].id == 1

    def test_find(self):
        self.mock_http_client.make_request.side_effect = [
            {'data': [{'id': 1, 'name': 'flag1'}], 'nextMarker': None}
        ]
        result = self.client.find(flag_set_name='flag1', workspace_id='workspace1')
        assert isinstance(result, FlagSet)
        assert result.id == 1

    def test_get(self):
        self.mock_http_client.make_request.return_value = {'id': 1, 'name': 'flag1'}
        result = self.client.get(flag_set_id='flag1')
        assert isinstance(result, FlagSet)
        assert result.id == 1

    def test_add(self):
        flag_set = FlagSet({'id': 1, 'name': 'flag1'}, self.mock_http_client)
        self.mock_http_client.make_request.return_value = {'id': 1, 'name': 'flag1'}
        result = self.client.add(flag_set, workspace_id='workspace1')
        assert isinstance(result, FlagSet)
        assert result.id == 1

    def test_delete(self):
        self.mock_http_client.make_request.return_value = True
        result = self.client.delete(flag_set_id='flag1')
        assert result is True