from flask_table import Table, Col


class Results(Table):
    id = Col('Id', show=False)
    numer = Col('Numer')
    stawka = Col('Stawka')
    wystawienie = Col('Wystawienie')
