from six import iteritems, integer_types, text_type
from datetime import datetime, date


parsed_dict = {
    'numer': 'string',
    'stawka': 'string',
    'data_wystawienia': 'string',
    'data_sprzedazy': 'string',
    'kwota': 'float',
    'sprzedawca': 'string',
    'nabywca': 'string'
}


class Wyniki(object):
    """Wyniki parsowania"""

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.                     
    """
    swagger_types = {
        'data_wystawienia': 'str',
        'data_sprzedazy': 'str',
        'stawka': 'str',
        'numer': 'str',
        'kwota': 'str',
        'sprzedawca': 'str',
        'nabywca': 'str'
    }

    attribute_map = {
        'data_wystawienia': 'dataWystawienia',
        'data_sprzedazy': 'dataSprzedazy',
        'stawka': 'stawka',
        'numer': 'numer',
        'kwota': 'kwota',
        'sprzedawca': 'sprzedawca',
        'nabywca': 'nabywca'
    }

    def __init__(self, data_wystawienia=None, data_sprzedazy=None, stawka=None, numer=None, kwota=None, sprzedawca=None,
                 nabywca=None):
        self.data_wystawienia = data_wystawienia
        self.data_sprzedazy = data_sprzedazy
        self.stawka = stawka
        self.numer = numer
        self.kwota = kwota
        self.sprzedawca = sprzedawca
        self.nabywca = nabywca


class ApiClient(object):

    PRIMITIVE_TYPES = (float, bool, bytes, text_type) + integer_types

    def __init__(self, host=None):
        """
        Constructor of the class.
        """
        if host is None:
            self.host = 'cesar'
        else:
            self.host = host

    def sanitize_for_serialization(self, obj):
        """
        Builds a JSON POST object.

        If obj is None, return None.
        If obj is str, int, long, float, bool, return directly.
        If obj is datetime.datetime, datetime.date
            convert to string in iso8601 format.
        If obj is list, sanitize each element in the list.
        If obj is dict, return the dict.
        If obj is swagger model, return the properties dict.

        :param obj: The data to serialize.
        :return: The serialized form of data.
        """
        if obj is None:
            return None
        elif isinstance(obj, self.PRIMITIVE_TYPES):
            return obj
        elif isinstance(obj, list):
            return [self.sanitize_for_serialization(sub_obj) for sub_obj in obj]
        elif isinstance(obj, tuple):
            return tuple(self.sanitize_for_serialization(sub_obj) for sub_obj in obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()

        if isinstance(obj, dict):
            obj_dict = obj
        else:
            # Convert model obj to dict except
            # attributes `swagger_types`, `attribute_map`
            # and attibutes which value is not None.
            # Convert attribute name to json key in
            # model definition for request.
            obj_dict = {obj.attribute_map[attr]: getattr(obj, attr)
                        for attr, _ in iteritems(obj.swagger_types)
                        if getattr(obj, attr) is not None}
        return {key: self.sanitize_for_serialization(val)
                for key, val in iteritems(obj_dict)}
