import abc


class BaseIdentifyClient:
    '''
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, config):
        pass

    @abc.abstractmethod
    def get_traffic_types(self):
        pass

    @abc.abstractmethod
    def get_environments(self):
        pass

    @abc.abstractmethod
    def get_attributes_for_traffic_type(self, traffic_type_id):
        pass

    @abc.abstractmethod
    def create_attribute_for_traffic_type(self, traffic_type_id, attr_data):
        pass

    @abc.abstractmethod
    def delete_attribute_from_schema(self, traffic_type_id, attribute_id):
        pass

    @abc.abstractmethod
    def add_identities(self, traffic_type_id, environment_id, entities):
        pass

    @abc.abstractmethod
    def add_identity(self, traffic_type_id, environment_id, key, values):
        pass

    @abc.abstractmethod
    def update_identity(self, traffic_type_id, environment_id, key, values):
        pass

    @abc.abstractmethod
    def patch_identity(self, traffic_type_id, environment_id, key, values):
        pass

    @abc.abstractmethod
    def delete_attributes_from_key(self, traffic_type_id, environment_id, key):
        pass
