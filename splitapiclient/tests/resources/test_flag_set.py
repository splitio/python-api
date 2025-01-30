import pytest
from unittest.mock import MagicMock, patch
from splitapiclient.resources.flag_set import FlagSet

class TestFlagSet:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_client = MagicMock()
        self.flag_set_data = {
            'id': 'flag1',
            'name': 'Test Flag',
            'description': 'Test Description',
            'workspace': {'id': 'workspace1', 'type': 'workspace'},
            'createdAt': '2023-01-01T00:00:00Z',
            'type': 'type1'
        }
        self.flag_set = FlagSet(data=self.flag_set_data, workspace_id='workspace1', client=self.mock_client)

    @patch('splitapiclient.resources.flag_set.require_client')
    def test_delete(self, mock_require_client):
        mock_require_client.return_value = self.mock_client
        self.mock_client.delete.return_value = True
        result = self.flag_set.delete(apiclient=self.mock_client)
        assert result is True
        self.mock_client.delete.assert_called_once_with('flag1')

    @patch('splitapiclient.resources.flag_set.require_client')
    def test_find(self, mock_require_client):
        mock_require_client.return_value = self.mock_client
        self.mock_client.find.return_value = self.flag_set_data
        result = self.flag_set.find(flagSetName='Test Flag', workspaceId='workspace1', apiclient=self.mock_client)
        assert result['id'] == 'flag1'
        assert result['name'] == 'Test Flag'
        self.mock_client.find.assert_called_once_with('Test Flag', 'workspace1')

    @patch('splitapiclient.resources.flag_set.require_client')
    def test_get(self, mock_require_client):
        mock_require_client.return_value = self.mock_client
        self.mock_client.get.return_value = self.flag_set_data
        result = self.flag_set.get(flagSetId='flag1', apiclient=self.mock_client)
        assert result['id'] == 'flag1'
        assert result['name'] == 'Test Flag'
        self.mock_client.get.assert_called_once_with('flag1')

    @patch('splitapiclient.resources.flag_set.require_client')
    def test_add(self, mock_require_client):
        mock_require_client.return_value = self.mock_client
        self.mock_client.add.return_value = self.flag_set_data
        result = self.flag_set.add(apiclient=self.mock_client)
        assert result['id'] == 'flag1'
        assert result['name'] == 'Test Flag'
        self.mock_client.add.assert_called_once_with('flag1', 'workspace1')

    @patch('splitapiclient.resources.flag_set.require_client')
    def test_list(self, mock_require_client):
        mock_require_client.return_value = self.mock_client
        self.mock_client.list.return_value = [self.flag_set_data]
        result = self.flag_set.list(workspaceId='workspace1', apiclient=self.mock_client)
        assert len(result) == 1
        assert result[0]['id'] == 'flag1'
        self.mock_client.list.assert_called_once_with('workspace1')