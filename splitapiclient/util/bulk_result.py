class BulkOperationResult:
    '''
    '''

    def __init__(self, successful=None, failed=None, metadata=None):
        '''
        '''
        self._successful = successful if successful else []
        self._failed = failed if failed else []
        self._metadata = metadata if metadata else {}

    @property
    def successful(self):
        return self._successful

    @property
    def failed(self):
        return self._failed

    @property
    def metadata(self):
        return self._metadata
