from __future__ import absolute_import, division, print_function, \
    unicode_literals

from splitapiclient.util.exceptions import InvalidArgumentException, \
    ClientRequiredError, InvalidModelException

def as_dict(data):
    '''
    '''
    from splitapiclient.resources.base_resource import BaseResource
    if isinstance(data, dict):
        return data
    elif isinstance(data, BaseResource):
        return data.to_dict()
    else:
        raise InvalidArgumentException(
            'Expencted a Resource instance or a dictionary containing '
            'resource properties as keys'
        )


def require_client(model, http_client, apiclient):
    '''
    '''
    from splitapiclient.main.apiclient import BaseApiClient
    from splitapiclient.http_clients.base_client import BaseHttpClient
    from splitapiclient.microclients.user_microclient import UserMicroClient
    from splitapiclient.microclients.group_microclient import GroupMicroClient
    from splitapiclient.microclients.attribute_microclient import AttributeMicroClient
    from splitapiclient.microclients.environment_microclient import EnvironmentMicroClient
    from splitapiclient.microclients.split_microclient import SplitMicroClient
    from splitapiclient.microclients.split_definition_microclient import SplitDefinitionMicroClient
    from splitapiclient.microclients.segment_microclient import SegmentMicroClient
    from splitapiclient.microclients.segment_definition_microclient import SegmentDefinitionMicroClient
    from splitapiclient.microclients.workspace_microclient import WorkspaceMicroClient
    from splitapiclient.microclients.identity_microclient import IdentityMicroClient
    from splitapiclient.microclients.traffic_type_microclient import TrafficTypeMicroClient
    from splitapiclient.microclients.change_request_microclient import ChangeRequestMicroClient
    from splitapiclient.microclients.apikey_microclient import APIKeyMicroClient
    from splitapiclient.microclients.restriction_microclient import RestrictionMicroClient

    if model not in ['Attribute', 'Workspace', 'Environment', 'Split', 'SplitDefinition', 'Segment', 'SegmentDefinition', 'Identity', 'TrafficType', 'ChangeRequest', 'User', 'Group', 'APIKey', 'Restriction']:
        raise InvalidModelException('Unknown model %s' % model)

    if apiclient and isinstance(apiclient, BaseApiClient):
        if model == 'Attribute': return apiclient.attributes
        if model == 'Environment': return apiclient.environments
        if model == 'Split': return apiclient.splits
        if model == 'SplitDefinition': return apiclient.split_definitions
        if model == 'Segment': return apiclient.segments
        if model == 'SegmentDefinition': return apiclient.segment_definitions
        if model == 'Workspace': return apiclient.workspaces
        if model == 'Identity': return apiclient.identities
        if model == 'TrafficType': return apiclient.traffic_types
        if model == 'ChangeRequest': return apiclient.change_requests
        if model == 'User': return apiclient.users
        if model == 'Group': return apiclient.groups
        if model == 'APIKey': return apiclient.apikeys
        if model == 'Restriction': return apiclient.restrictions
    elif http_client and isinstance(http_client, BaseHttpClient):
        if model == 'Attribute': return AttributeMicroClient(http_client)
        if model == 'Environment': return EnvironmentMicroClient(http_client)
        if model == 'SplitDefinition': return SplitDefinitionMicroClient(http_client)
        if model == 'Split': return SplitMicroClient(http_client)
        if model == 'Segment': return SegmentMicroClient(http_client)
        if model == 'SegmentDefinition': return SegmentDefinitionMicroClient(http_client)
        if model == 'Workspace': return WorkspaceMicroClient(http_client)
        if model == 'Identity': return IdentityMicroClient(http_client)
        if model == 'TrafficType': return TrafficTypeMicroClient(http_client)
        if model == 'ChangeRequest': return ChangeRequestMicroClient(http_client)
        if model == 'User': return UserMicroClient(http_client)
        if model == 'Group': return GroupMicroClient(http_client)
        if model == 'APIKey': return APIKeyMicroClient(http_client)
        if model == 'Restriction': return RestrictionMicroClient(http_client)
    else:
        raise ClientRequiredError(
            'Object created ad-hoc, you need to pass a SplitApiClient instance '
            'for the http call to be made'
        )
