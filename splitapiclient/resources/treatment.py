from __future__ import absolute_import, division, print_function, \
    unicode_literals

class Treatment():
    '''
    '''
    _schema = {
        'name': 'string',
        'configurations': 'string',
        'description': 'string',
        'keys': [ 'string' ],
        'segments': [ 'string' ]
    }

    def __init__(self, data=None):
        '''
        '''
        if not data:
            data = {}
        self._name = data.get('name')
        self._description = data.get('description') if 'description' in data else ""
        self._configurations = data.get('configurations') if 'configurations' in data else ""
        self._keys = []
        if 'keys' in data:
            for item in data.get('keys'):
                self._keys.append(item)
        self._segments = []
        if 'segments' in data:
            for item in data.get('segments'):
                self._segments.append(item)

    def export_dict(self):
        result = {'name':self._name}
        if self._description != "":
            result['description'] = self._description
        if self._configurations != "":
            result['configurations'] = self._configurations
        if len(self._keys)>0:
            result['keys'] = self._keys
        if len(self._segments)>0:
            result['segments'] = self._segments
        return result
