"""
Shared pytest fixtures and helpers for Harness microclient tests.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest


class FakeResponse:
    """
    Simple class to mock Response objects from the requests module.
    Used for testing URL generation without making actual HTTP calls.
    """
    def __init__(self, status, text):
        self.status_code = status
        self.text = text


@pytest.fixture
def fake_response():
    """Factory fixture for creating FakeResponse objects."""
    def _create_response(status=200, text='{}'):
        return FakeResponse(status, text)
    return _create_response


@pytest.fixture
def mock_requests_get(mocker):
    """Mock requests.get and return the mock for assertions."""
    mock = mocker.patch('splitapiclient.http_clients.sync_client.requests.get')
    mock.return_value = FakeResponse(200, '{"data": []}')
    return mock


@pytest.fixture
def mock_requests_post(mocker):
    """Mock requests.post and return the mock for assertions."""
    mock = mocker.patch('splitapiclient.http_clients.sync_client.requests.post')
    mock.return_value = FakeResponse(200, '{"data": {}}')
    return mock


@pytest.fixture
def mock_requests_put(mocker):
    """Mock requests.put and return the mock for assertions."""
    mock = mocker.patch('splitapiclient.http_clients.sync_client.requests.put')
    mock.return_value = FakeResponse(200, '{"data": {}}')
    return mock


@pytest.fixture
def mock_requests_delete(mocker):
    """Mock requests.delete and return the mock for assertions."""
    mock = mocker.patch('splitapiclient.http_clients.sync_client.requests.delete')
    mock.return_value = FakeResponse(200, '{}')
    return mock

