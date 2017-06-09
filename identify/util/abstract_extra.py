from __future__ import absolute_import, division, print_function, \
    unicode_literals
import sys
import abc


class StaticAbstractV2(staticmethod):
    '''
    TODO
    '''
    __slots__ = ()
    __isabstractmethod__ = True

    def __init__(self, fn):
        '''
        TODO
        '''
        staticmethod.__init__(self, fn)
        fn.__isabstractmethod__ = True


class ClassAbstractV2(classmethod):
    '''
    TODO
    '''
    __slots__ = ()
    __isabstractmethod__ = True

    def __init__(self, fn):
        '''
        TODO
        '''
        classmethod.__init__(self, fn)
        fn.__isabstractmethod__ = True


if sys.version_info <= (3, 0):
    staticabstract = StaticAbstractV2
    classabstract = ClassAbstractV2
else:
    staticabstract = abc.abstractstaticmethod
    classabstract = abc.abstractclassmethod
