from __future__ import absolute_import, division, print_function, \
    unicode_literals

class Matcher():
    '''
    '''
    _schema = {
        'negate': 'boolean',
        'type': 'string',
        'attribute': 'string',
        'string': 'string',
        'bool' : 'boolean',
        'strings' : [ 'string' ],
        'number' : 'number',
        'date' : 'number',
        'between': {
            'from': 'number',
            'to' : 'number'
        },
        'depends': {
            'splitName': 'string',
            'treatment': 'string'
        }
    }

    def __init__(self, data=None):
        '''
        '''
        if not data:
            data = {}
        self._negate = data.get('negate') if 'negate' in data else ""
        self._type = data.get('type') if 'type' in data else ""
        self._attribute = data.get('attribute') if 'attribute' in data else ""
        self._string = data.get('string') if 'string' in data else ""
        self._bool = data.get('bool') if 'bool' in data else ""
        self._strings = []
        if 'strings' in data:
            for item in data.get('strings'):
                self._strings.append(item)
        self._number = data.get('number') if 'number' in data else ""
        self._date = data.get('date') if 'date' in data else ""
        self._between = data.get('between') if 'between' in data else {}
        self._depends = data.get('depends') if 'depends' in data else {}
        
    def export_dict(self):
        result = {}
        if self._negate != "":
            result['negate'] = self._negate
        if self._type != "":
            result['type'] = self._type
        if self._attribute != "":
            result['attribute'] = self._attribute
        if self._string != "":
            result['string'] = self._string
        if self._bool != "":
            result['bool'] = self._bool
        if len(self._strings)>0:
            result['strings'] = self._strings
        if self._number != "":
            result['number'] = self._number
        if self._date != "":
            result['date'] = self._date
        if len(self._between)>0:
            result['between'] = self._between
        if len(self._depends)>0:
            result['depends'] = self._depends
        return result



