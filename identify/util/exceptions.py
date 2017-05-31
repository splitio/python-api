class HTTPResponseError(Exception):
    '''
    Exception to be thrown when the API call's status code is not 200.
    '''
    def __init__(self, message, response):
        '''
        '''
        Exception.__init__(self, message)
        self._error = response


class EndpointNotImplemented(Exception):
    '''
    Exception to be thrown when the requested endpoint is not available for
    a particular resource
    '''
    pass


class MethodNotApplicable(Exception):
    '''
    Exception to be thrown when a class method is called in a class that
    shouldn't. For example the Identity Resource doesn't have an endpoint
    that returns all items, hence calling `_process_single_response` on it
    makes no sense.
    '''
    pass
