class IdentifyException(Exception):
    '''
    Identify Base Exception class that can be used to catch all identify-related
    exceptions in a single block.
    '''


class HTTPResponseError(IdentifyException):
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


class EndpointNotImplemented(IdentifyException):
    '''
    Exception to be thrown when the requested endpoint is not available for
    a particular resource
    '''
    pass


class MethodNotApplicable(IdentifyException):
    '''
    Exception to be thrown when a class method is called in a class that
    shouldn't. For example the Identity Resource doesn't have an endpoint
    that returns all items, hence calling `_process_single_response` on it
    makes no sense.
    '''
    pass


class MissingParametersException(IdentifyException):
    '''
    Exception to be thown when one or more parameters required for a certain
    endpoint weren't passed at the moment of making a request.
    '''
    pass


class InsufficientConfigArgumentsException(IdentifyException):
    '''
    Exception to be thrown when a the configuration doesn't have all the
    required arguments (currently `base_url` and `apikey`.
    '''
    pass


class UnknownIdentifyClientError(IdentifyException):
    '''
    Exception to be thrown when an unexpected error (most probably a bug)
    happens
    '''
    pass
