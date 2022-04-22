from __future__ import absolute_import, division, print_function, \
    unicode_literals
import abc


class BaseApiClient:
    '''
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, config):
        pass

    @abc.abstractproperty
    def traffic_types(self):
        pass

    @abc.abstractproperty
    def environments(self):
        pass

    @abc.abstractproperty
    def splits(self):
        pass

    @abc.abstractproperty
    def split_definitions(self):
        pass

    @abc.abstractproperty
    def segments(self):
        pass

    @abc.abstractproperty
    def segment_definitions(self):
        pass

    @abc.abstractproperty
    def workspaces(self):
        pass

    
    @abc.abstractproperty
    def attributes(self):
        pass

    @abc.abstractproperty
    def identities(self):
        pass

    @abc.abstractproperty
    def change_requests(self):
        pass

    @abc.abstractproperty
    def users(self):
        pass

    @abc.abstractproperty
    def groups(self):
        pass

    @abc.abstractproperty
    def apikeys(self):
        pass

    @abc.abstractproperty
    def restrictions(self):
        pass
