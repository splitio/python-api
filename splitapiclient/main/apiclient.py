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
    def environments(sself):
        pass

    @abc.abstractproperty
    def attributes(self):
        pass

    @abc.abstractproperty
    def identities(self):
        pass
