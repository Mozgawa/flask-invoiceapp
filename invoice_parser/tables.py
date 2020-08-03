from flask_table import Table, Col


class Results(Table):
    def sort_url(self, col_id, reverse=False):
        pass

    id = Col('Id', show=False)
    numer = Col('Numer')
    stawka = Col('Stawka')
    wystawienie = Col('Wystawienie')
    sprzedaz = Col('Sprzedaz')
    kwota = Col('Kwota')
    sprzedawca = Col('Sprzedawca')
    nabywca = Col('Nabywca')
