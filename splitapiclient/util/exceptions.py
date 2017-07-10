from __future__ import absolute_import, division, print_function, \
    unicode_literals


class SplitException(Exception):
    '''
    SplitException class that can be used to catch all identify-related
    exceptions in a single block.
    '''


class HTTPResponseError(SplitException):
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


class EndpointNotImplemented(SplitException):
    '''
    Exception to be thrown when the requested endpoint is not available for
    a particular resource
    '''
    pass


class MethodNotApplicable(SplitException):
    '''
    Exception to be thrown when a class method is called in a class that
    shouldn't. For example the Identity Resource doesn't have an endpoint
    that returns all items, hence calling `_process_single_response` on it
    makes no sense.
    '''
    pass


class MissingParametersException(SplitException):
    '''
    Exception to be thown when one or more parameters required for a certain
    endpoint weren't passed at the moment of making a request.
    '''
    pass


class InsufficientConfigArgumentsException(SplitException):
    '''
    Exception to be thrown when a the configuration doesn't have all the
    required arguments (currently `base_url` and `apikey`.
    '''
    pass


class UnknownApiClientError(SplitException):
    '''
    Exception to be thrown when an unexpected error (most probably a bug)
    happens
    '''
    pass


class ClientRequiredError(SplitException):
    '''
    Exception to be thrown when an operation that requires an http client has
    been attempted but the object was created with the constructor directly
    and no client was passed.
    '''
    pass


class SplitBackendUnreachableError(SplitException):
    '''
    Exception to be thrown when the Split API cannot be reached, usually
    due a a connection error, or an incorrect baseUrl
    '''
    pass


class InvalidArgumentException(SplitException):
    '''
    This exception will be thrown when a method expected an argument of a
    different type
    '''
    pass

class InvalidModelException(SplitException):
    '''
    Exception to be thrown when an invalid model is used when attempting to
    retrieve a client
    '''
    pass
