from invoiceapp import db


class Faktura(db.Model):
    __tablename__ = 'faktury'

    id = db.Column(db.Integer, primary_key=True)
    numer = db.Column(db.String())
    stawka = db.Column(db.String())
    wystawienie = db.Column(db.String())

    def __init__(self, numer, stawka, wystawienie):
        self.numer = numer
        self.stawka = stawka
        self.wystawienie = wystawienie

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'numer': self.numer,
            'stawka': self.stawka,
            'wystawienie': self.wystawienie
        }