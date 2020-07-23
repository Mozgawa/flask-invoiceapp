from six import iteritems, integer_types, text_type
from datetime import datetime, date


parsed_dict = {
    'nr_faktury': 'string',
    'sprzedawca': {
        'nazwa': 'string',
        'adres': 'string',
        'nip': 'string',
        'forma': 'string'
    },
    'nabywca': {
        'nazwa': 'string',
        'adres': 'string',
        'nip': 'string',
        'forma': 'string'
    },
    'data_wystawienia': 'string',
    'data_sprzedazy': 'string',
    'towar_usluga': 'string',
    'netto': 'float',
    'brutto': 'float',
    'podatek': 'string',
    'naleznosc': 'string',
    'stawka': 'string'
}


class Stawka(object):
    """Stawka"""

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.                     
    """
    swagger_types = {
        'stawka': 'str',
        'zgodna': 'bool'
    }

    attribute_map = {
        'stawka': 'stawka',
        'zgodna': 'zgodna'
    }

    def __init__(self, stawka=None, zgodna=None):
        self.stawka = stawka
        self.zgodna = zgodna


class Kwota(object):
    """Kwota"""

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.                     
    """
    swagger_types = {
        'brutto': 'str',
        'netto': 'str',
        'vat': 'str',
        'waluta': 'str'
    }

    attribute_map = {
        'brutto': 'brutto',
        'netto': 'netto',
        'vat': 'vat',
        'waluta': 'waluta'
    }

    def __init__(self, brutto=None, netto=None, vat=None, waluta=None):
        self.brutto = brutto
        self.netto = netto
        self.vat = vat
        self.waluta = waluta


class Adres(object):
    """Wyniki parsowania"""

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.                     
    """
    swagger_types = {
        'miejscowosc': 'str',
        'kod_pocztowy': 'str',
        'ulica': 'str',
        'nr_budynku': 'str',
        'nr_mieszkania': 'str'
    }

    attribute_map = {
        'miejscowosc': 'miejscowosc',
        'kod_pocztowy': 'kodPocztowy',
        'ulica': 'ulica',
        'nr_budynku': 'nrBudynku',
        'nr_mieszkania': 'nrMieszkania',
    }

    def __init__(self, miejscowosc=None, kod_pocztowy=None, ulica=None, nr_budynku=None, nr_mieszkania=None):
        self.miejscowosc = miejscowosc
        self.kod_pocztowy = kod_pocztowy
        self.ulica = ulica
        self.nr_budynku = nr_budynku
        self.nr_mieszkania = nr_mieszkania


class Podmiot(object):
    """Podmiot prawa cywilnego. Osoba Prawna lub Osoba Fizyczna. Np. Sprzedawca, nabywca"""

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.                     
    """
    swagger_types = {
        'nazwa': 'str',
        'adres': 'str',
        'nip': 'int',
        'forma': 'str'
    }

    attribute_map = {
        'nazwa': 'nazwa',
        'adres': 'adres',
        'nip': 'nip',
        'forma': 'forma'
    }

    def __init__(self, nazwa=None, adres=None, nip=None, forma=None):
        self.nazwa = nazwa
        self.adres = adres
        self.nip = nip
        self.forma = forma


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
        'nip': 'list[int]',
        'numer': 'str',
        'kwota': 'str',
        'sprzedawca': 'Podmiot',
        'nabywca': 'Podmiot'
    }

    attribute_map = {
        'data_wystawienia': 'dataWystawienia',
        'data_sprzedazy': 'dataSprzedazy',
        'stawka': 'stawka',
        'nip': 'nip',
        'numer': 'numer',
        'kwota': 'kwota',
        'sprzedawca': 'sprzedawca',
        'nabywca': 'nabywca'
    }


    def __init__(self, data_wystawienia=None, data_sprzedazy=None, stawka=None, nip=None, numer=None, kwota=None, sprzedawca=None, nabywca=None):
        self.data_wystawienia = data_wystawienia
        self.data_sprzedazy = data_sprzedazy
        self.stawka = stawka
        self.nip = nip
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
