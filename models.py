from invoiceapp import db


class Faktura(db.Model):
    __tablename__ = 'faktury'

    id = db.Column(db.Integer, primary_key=True)
    numer = db.Column(db.String())
    stawka = db.Column(db.String())
    wystawienie = db.Column(db.String())
    sprzedaz = db.Column(db.String())
    kwota = db.Column(db.String())
    sprzedawca = db.Column(db.String())
    nabywca = db.Column(db.String())

    def __init__(self, numer, stawka, wystawienie, sprzedaz, kwota, sprzedawca, nabywca):
        self.numer = numer
        self.stawka = stawka
        self.wystawienie = wystawienie
        self.sprzedaz = sprzedaz
        self.kwota = kwota
        self.sprzedawca = sprzedawca
        self.nabywca = nabywca

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'numer': self.numer,
            'stawka': self.stawka,
            'wystawienie': self.wystawienie,
            'sprzedaz': self.sprzedaz,
            'kwota': self.kwota,
            'sprzedawca': self.sprzedawca,
            'nabywca': self.nabywca
        }
