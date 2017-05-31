import abc
import six
from identify.util import validation
from identify.util.logger import LOGGER
from identify.util.abstract_extra import classabstract_v2
from identify.util.exceptions import HTTPResponseError, EndpointNotImplemented


class BaseResource:
    '''
    Abstract class to handle resources uniformely.
    '''

    __metaclass__ = abc.ABCMeta

    def __init__(self, client, id):
        '''
        Constructs (a child) resource instance (called via super or __init__,
        stores the id and client.

        :param id: string. Resource Id.
        :param client: HTTP client that will be used to make API calls.
        '''
        self._id = id
        self._client = client

    @abc.abstractproperty
    def _endpoint(self):
        pass

    @abc.abstractproperty
    def _schema(self):
        pass

    @classmethod
    def _process_all_response(cls, client, response):
        '''
        This method simply calls the child (concrete) class' appropriate method
        for constructing a resource object out of a single item extracted from
        a returned collection.

        :param client: HTTP Client
        :param response: response received from the API

        :rtype: list
        '''
        LOGGER.debug("Proccesing {n} items".format(n=len(response)))
        return [
            cls._build_single_from_collection_response(client, item)
            for item in response # .get('objects', [])
        ]

    @classabstract_v2
    def _build_single_from_collection_response(cls, client, response):
        '''
        Abstract Class method to construct a resource instance from a single
        item extracted from a colleciton.
        '''
        pass

    @classmethod
    def retrieve_single(cls, client, **kwargs):
        '''
        NOT USED. DECIDE IF NECESSARY
        '''
        try:
            response = client.get(cls._endpoint['single_item'], **kwargs)
            return response
        except:
            import traceback
            traceback.print_exc()

    @classmethod
    def retrieve_all(cls, client, **kwargs):
        '''
        Class method that uses the child class' 'all_items' endpoint if
        available to retrieve all items.

        :param client: HTTP Client.
        :param kwargs: Other parameters required to make that request.

        :rtype: list
        '''
        endpoint = cls._endpoint.get('all_items')
        if not endpoint:
            raise EndpointNotImplemented

        try:
            response = client.make_request(endpoint, **kwargs)
            return cls._process_all_response(client, response)
        except HTTPResponseError:
            LOGGER.error('Call to Identify API failed, returning empty result')
            return []
        except:
            LOGGER.error('Unknown failure. Returning empty result')
            import traceback
            traceback.print_exc()
            return []

    @classmethod
    def _validate(cls, response_item):
        '''
        This method validates that the schema from an object returned by the API
        matches the schema defined for the requested resource, defined in the
        child class.

        :param response_item: dict. Single item to verify.
        '''
        return all(
            validation.is_correct_type(value, cls._schema.get(key))
            for key, value in six.iteritems(response_item)
        )
