class staticabstract_v2(staticmethod):
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


class classabstract_v2(classmethod):
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
