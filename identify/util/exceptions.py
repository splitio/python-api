class HTTPResponseError(Exception):
    '''
    Exception to be thrown when the API call's status code is not 200.
    '''
    def __init__(self, message=None, response=None):
        '''
        '''
        Exception.__init__(self, message)
        self._error = response


class HTTPUnauthorizedError(HTTPResponseError):
    pass


class HTTPNotFoundError(HTTPResponseError):
    pass


class HTTPIncorrectParametersError(HTTPResponseError):
    pass


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


class MissingParametersException(Exception):
    '''
    Exception to be thown when one or more parameters required for a certain
    endpoint weren't passed at the moment of making a request.
    '''
    pass
