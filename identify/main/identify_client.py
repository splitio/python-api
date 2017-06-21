from __future__ import absolute_import, division, print_function, \
    unicode_literals
import abc


class BaseIdentifyClient:
    '''
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, config):
        pass

    @abc.abstractproperty
    def traffic_type(self):
        pass

    @abc.abstractproperty
    def environment(self):
        pass

    @abc.abstractproperty
    def attribute(self):
        pass

    @abc.abstractproperty
    def identity(self):
        pass
