from splitapiclient.resources.base_resource import BaseResource
from splitapiclient.util.exceptions import InvalidArgumentException

def as_dict(data):
    '''
    '''
    if isinstance(data, dict):
        return data
    elif isinstance(data, BaseResource):
        return data.to_dict()
    else:
        raise InvalidArgumentException(
            'Expencted a Resource instance or a dictionary containing '
            'resource properties as keys'
        )



