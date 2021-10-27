from __future__ import absolute_import, division, print_function, \
    unicode_literals

class DefaultRule():
    '''
    '''
    _schema = {
        'treatment': 'string',
        'size': 'number'
    }

    def __init__(self, data=None, client=None):
        '''
        '''
        if not data:
            data = {}
        self._treatment = data.get('treatment')
        self._size = data.get('size')
                    
    def export_dict(self):
        return {'treatment':self._treatment, 'size':self._size}
