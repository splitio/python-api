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
    from splitapiclient.microclients.attribute_microclient import AttributeMicroClient
    from splitapiclient.microclients.environment_microclient import EnvironmentMicroClient
    from splitapiclient.microclients.identity_microclient import IdentityMicroClient
    from splitapiclient.microclients.traffic_type_microclient import TrafficTypeMicroClient

    if model not in ['Attribute', 'Environment', 'Identity', 'TrafficType']:
        raise InvalidModelException('Unknown model %s' % model)

    if apiclient and isinstance(apiclient, BaseApiClient):
        if model == 'Attribute': return apiclient.attributes
        if model == 'Environment': return apiclient.environments
        if model == 'Identity': return apiclient.identities
        if model == 'TrafficType': return apiclient.traffic_types
    elif http_client and isinstance(http_client, BaseHttpClient):
        if model == 'Attribute': return AttributeMicroClient(http_client)
        if model == 'Environment': return EnvironmentMicroClient(http_client)
        if model == 'Identity': return IdentityMicroClient(http_client)
        if model == 'TrafficType': return TrafficTypeMicroClient(http_client)
    else:
        raise ClientRequiredError(
            'Object created ad-hoc, you need to pass a SplitApiClient instance '
            'for the http call to be made'
        )
