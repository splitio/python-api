from __future__ import absolute_import, division, print_function, \
    unicode_literals

import pytest
from splitapiclient.microclients.harness import (
    HarnessProjectMicroClient,
    ServiceAccountMicroClient,
    TokenMicroClient,
    HarnessApiKeyMicroClient,
    HarnessUserMicroClient,
    HarnessGroupMicroClient,
    RoleMicroClient,
    ResourceGroupMicroClient,
    RoleAssignmentMicroClient
)
from splitapiclient.http_clients.sync_client import SyncHttpClient


class TestOptionalIdentifiers:
    """
    Test that orgIdentifier and projectIdentifier are only included in URLs when they are set.
    """

    def test_list_without_org_and_project_identifiers(self, mocker):
        """
        Test that when org_identifier and project_identifier are not set,
        they are not included in the URL.
        """
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        pmc = HarnessProjectMicroClient(sc, 'test_account')
        
        # Mock empty response
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        
        # Call list without org or project identifiers
        pmc.list()
        
        # Verify the URL template does not contain orgIdentifier or projectIdentifier
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' not in url_template
        assert 'projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template
        
        # Verify request_kwargs does not include orgIdentifier or projectIdentifier
        request_kwargs = call_args[1]
        assert 'orgIdentifier' not in request_kwargs
        assert 'projectIdentifier' not in request_kwargs
        assert 'accountIdentifier' in request_kwargs

    def test_list_with_org_identifier_only(self, mocker):
        """
        Test that when only org_identifier is set, only orgIdentifier is in the URL.
        """
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        pmc = HarnessProjectMicroClient(sc, 'test_account', org_identifier='test_org')
        
        # Mock empty response
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        
        # Call list
        pmc.list()
        
        # Verify the URL template contains orgIdentifier but not projectIdentifier
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' in url_template
        assert 'projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template
        
        # Verify request_kwargs includes orgIdentifier but not projectIdentifier
        request_kwargs = call_args[1]
        assert 'orgIdentifier' in request_kwargs
        assert request_kwargs['orgIdentifier'] == 'test_org'
        assert 'projectIdentifier' not in request_kwargs
        assert 'accountIdentifier' in request_kwargs

    def test_list_with_project_identifier_only(self, mocker):
        """
        Test that project_identifier is NOT used for projects list endpoint.
        Note: The projects endpoint does not support projectIdentifier as a query parameter.
        """
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        pmc = HarnessProjectMicroClient(sc, 'test_account', project_identifier='test_project')
        
        # Mock empty response
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        
        # Call list
        pmc.list()
        
        # Verify the URL template does NOT contain projectIdentifier (projects endpoint doesn't support it)
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'projectIdentifier' not in url_template
        assert 'orgIdentifier' not in url_template
        assert 'accountIdentifier' in url_template
        
        # Verify request_kwargs does NOT include projectIdentifier
        request_kwargs = call_args[1]
        assert 'projectIdentifier' not in request_kwargs
        assert 'orgIdentifier' not in request_kwargs
        assert 'accountIdentifier' in request_kwargs

    def test_list_with_both_identifiers(self, mocker):
        """
        Test that when both org_identifier and project_identifier are set,
        only orgIdentifier is in the URL (projects endpoint doesn't support projectIdentifier).
        """
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        pmc = HarnessProjectMicroClient(sc, 'test_account', org_identifier='test_org', project_identifier='test_project')
        
        # Mock empty response
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        
        # Call list
        pmc.list()
        
        # Verify the URL template contains orgIdentifier but NOT projectIdentifier
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' in url_template
        assert 'projectIdentifier' not in url_template  # Projects endpoint doesn't support this
        assert 'accountIdentifier' in url_template
        
        # Verify request_kwargs includes orgIdentifier but NOT projectIdentifier
        request_kwargs = call_args[1]
        assert 'orgIdentifier' in request_kwargs
        assert request_kwargs['orgIdentifier'] == 'test_org'
        assert 'projectIdentifier' not in request_kwargs  # Projects endpoint doesn't support this
        assert 'accountIdentifier' in request_kwargs

    def test_list_with_method_override(self, mocker):
        """
        Test that method parameters override instance variables when set to non-None values.
        Note: Passing None as a method parameter does NOT override instance variables
        (this is current behavior - if you want to unset, don't pass the parameter).
        Note: project_identifier is NOT used for projects list endpoint.
        """
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        # Initialize with org_identifier but not project_identifier
        pmc = HarnessProjectMicroClient(sc, 'test_account', org_identifier='default_org')
        
        # Mock empty response
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        
        # Call list with method-level org_identifier override
        pmc.list(org_identifier='method_org')
        
        # Verify the URL template contains orgIdentifier (from method override) but NOT projectIdentifier
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'projectIdentifier' not in url_template  # Projects endpoint doesn't support this
        assert 'orgIdentifier' in url_template  # Uses method override
        
        # Verify request_kwargs
        request_kwargs = call_args[1]
        assert 'projectIdentifier' not in request_kwargs  # Projects endpoint doesn't support this
        assert 'orgIdentifier' in request_kwargs
        assert request_kwargs['orgIdentifier'] == 'method_org'  # From method override

    def test_get_without_org_and_project_identifiers(self, mocker):
        """
        Test get method without org and project identifiers.
        """
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        pmc = HarnessProjectMicroClient(sc, 'test_account')
        
        # Mock response
        SyncHttpClient.make_request.return_value = {
            'data': {'project': {'identifier': 'proj1', 'name': 'Project 1'}}
        }
        
        # Call get
        pmc.get('proj1')
        
        # Verify the URL template does not contain orgIdentifier or projectIdentifier query params
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        # Note: projectIdentifier is in the path, but not as a query param when not set
        assert '&orgIdentifier' not in url_template
        assert '&projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template
        
        # Verify request_kwargs
        request_kwargs = call_args[1]
        assert 'orgIdentifier' not in request_kwargs
        # projectIdentifier is in request_kwargs as path parameter, but not as query param
        assert 'accountIdentifier' in request_kwargs

    def test_create_with_org_identifier_only(self, mocker):
        """
        Test create method with only org_identifier set.
        """
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        pmc = HarnessProjectMicroClient(sc, 'test_account', org_identifier='test_org')
        
        # Mock response
        SyncHttpClient.make_request.return_value = {
            'data': {'project': {'identifier': 'new_proj', 'name': 'New Project'}}
        }
        
        # Call create
        pmc.create({'name': 'New Project'})
        
        # Verify the URL template contains orgIdentifier but not projectIdentifier
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' in url_template
        assert 'projectIdentifier' not in url_template
        
        # Verify request_kwargs
        request_kwargs = call_args[1]
        assert 'orgIdentifier' in request_kwargs
        assert request_kwargs['orgIdentifier'] == 'test_org'
        assert 'projectIdentifier' not in request_kwargs

    def test_service_account_list_with_both_identifiers(self, mocker):
        """
        Test service account list with both identifiers to verify pattern works across microclients.
        """
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        samc = ServiceAccountMicroClient(sc, 'test_account', org_identifier='test_org', project_identifier='test_project')
        
        # Mock response
        SyncHttpClient.make_request.return_value = {'data': []}
        
        # Call list
        samc.list()
        
        # Verify the URL template contains both
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' in url_template
        assert 'projectIdentifier' in url_template
        
        # Verify request_kwargs includes both
        request_kwargs = call_args[1]
        assert 'orgIdentifier' in request_kwargs
        assert request_kwargs['orgIdentifier'] == 'test_org'
        assert 'projectIdentifier' in request_kwargs
        assert request_kwargs['projectIdentifier'] == 'test_project'

    def test_service_account_list_without_identifiers(self, mocker):
        """
        Test service account list without identifiers.
        """
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        samc = ServiceAccountMicroClient(sc, 'test_account')
        
        # Mock response
        SyncHttpClient.make_request.return_value = {'data': []}
        
        # Call list
        samc.list()
        
        # Verify the URL template does not contain orgIdentifier or projectIdentifier
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' not in url_template
        assert 'projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template
        
        # Verify request_kwargs
        request_kwargs = call_args[1]
        assert 'orgIdentifier' not in request_kwargs
        assert 'projectIdentifier' not in request_kwargs
        assert 'accountIdentifier' in request_kwargs

    def test_token_list_without_identifiers(self, mocker):
        """Test token list without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        tmc = TokenMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        tmc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' not in url_template
        assert 'projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

    def test_token_list_with_both_identifiers(self, mocker):
        """Test token list with both identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        tmc = TokenMicroClient(sc, 'test_account', org_identifier='test_org', project_identifier='test_project')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        tmc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' in url_template
        assert 'projectIdentifier' in url_template

    def test_harness_apikey_list_without_identifiers(self, mocker):
        """Test harness apikey list without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        akmc = HarnessApiKeyMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': []}
        akmc.list('parent1')
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' not in url_template
        assert 'projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

    def test_harness_apikey_list_with_both_identifiers(self, mocker):
        """Test harness apikey list with both identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        akmc = HarnessApiKeyMicroClient(sc, 'test_account', org_identifier='test_org', project_identifier='test_project')
        
        SyncHttpClient.make_request.return_value = {'data': []}
        akmc.list('parent1')
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' in url_template
        assert 'projectIdentifier' in url_template

    def test_harness_user_list_without_identifiers(self, mocker):
        """Test harness user list without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        umc = HarnessUserMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        umc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' not in url_template
        assert 'projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

    def test_harness_user_list_with_both_identifiers(self, mocker):
        """Test harness user list with both identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        umc = HarnessUserMicroClient(sc, 'test_account', org_identifier='test_org', project_identifier='test_project')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        umc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' in url_template
        assert 'projectIdentifier' in url_template

    def test_harness_user_get_without_identifiers(self, mocker):
        """Test harness user get without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        umc = HarnessUserMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'user': {'uuid': 'user1', 'name': 'User 1'}}}
        umc.get('user1')
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert '&orgIdentifier' not in url_template
        assert '&projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

    def test_harness_group_list_without_identifiers(self, mocker):
        """Test harness group list without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        gmc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' not in url_template
        assert 'projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

    def test_harness_group_list_with_both_identifiers(self, mocker):
        """Test harness group list with both identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account', org_identifier='test_org', project_identifier='test_project')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        gmc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' in url_template
        assert 'projectIdentifier' in url_template

    def test_harness_group_get_without_identifiers(self, mocker):
        """Test harness group get without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        gmc = HarnessGroupMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'identifier': 'group1', 'name': 'Group 1'}}
        gmc.get('group1')
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert '&orgIdentifier' not in url_template
        assert '&projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

    def test_role_list_without_identifiers(self, mocker):
        """Test role list without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rmc = RoleMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        rmc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' not in url_template
        assert 'projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

    def test_role_list_with_both_identifiers(self, mocker):
        """Test role list with both identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rmc = RoleMicroClient(sc, 'test_account', org_identifier='test_org', project_identifier='test_project')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        rmc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' in url_template
        assert 'projectIdentifier' in url_template

    def test_role_get_without_identifiers(self, mocker):
        """Test role get without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rmc = RoleMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'role': {'identifier': 'role1', 'name': 'Role 1'}}}
        rmc.get('role1')
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        # Role get endpoint doesn't have org/project in URL template
        assert 'accountIdentifier' in url_template

    def test_resource_group_list_without_identifiers(self, mocker):
        """Test resource group list without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rgmc = ResourceGroupMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        rgmc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' not in url_template
        assert 'projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

    def test_resource_group_list_with_both_identifiers(self, mocker):
        """Test resource group list with both identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rgmc = ResourceGroupMicroClient(sc, 'test_account', org_identifier='test_org', project_identifier='test_project')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        rgmc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' in url_template
        assert 'projectIdentifier' in url_template

    def test_resource_group_get_without_identifiers(self, mocker):
        """Test resource group get without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        rgmc = ResourceGroupMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'resourceGroup': {'identifier': 'rg1', 'name': 'RG 1'}}}
        rgmc.get('rg1')
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert '&orgIdentifier' not in url_template
        assert '&projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

    def test_role_assignment_list_without_identifiers(self, mocker):
        """Test role assignment list without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        ramc = RoleAssignmentMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        ramc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' not in url_template
        assert 'projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

    def test_role_assignment_list_with_both_identifiers(self, mocker):
        """Test role assignment list with both identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        ramc = RoleAssignmentMicroClient(sc, 'test_account', org_identifier='test_org', project_identifier='test_project')
        
        SyncHttpClient.make_request.return_value = {'data': {'content': []}}
        ramc.list()
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert 'orgIdentifier' in url_template
        assert 'projectIdentifier' in url_template

    def test_role_assignment_get_without_identifiers(self, mocker):
        """Test role assignment get without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        ramc = RoleAssignmentMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'roleAssignment': {'identifier': 'ra1'}}}
        ramc.get('ra1')
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert '&orgIdentifier' not in url_template
        assert '&projectIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

    def test_service_account_get_without_identifiers(self, mocker):
        """Test service account get without identifiers."""
        mocker.patch('splitapiclient.http_clients.sync_client.SyncHttpClient.make_request')
        sc = SyncHttpClient('abc', 'abc')
        samc = ServiceAccountMicroClient(sc, 'test_account')
        
        SyncHttpClient.make_request.return_value = {'data': {'serviceAccount': {'identifier': 'sa1', 'name': 'SA 1'}}}
        samc.get('sa1')
        
        call_args = SyncHttpClient.make_request.call_args
        endpoint = call_args[0][0]
        url_template = endpoint['url_template']
        
        assert '&orgIdentifier' not in url_template
        assert 'accountIdentifier' in url_template

