import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Faktura

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/add")
def add_book():
    numer=request.args.get('numer')
    stawka=request.args.get('stawka')
    wystawienie=request.args.get('wystawienie')
    try:
        faktura=Faktura(
            numer=numer,
            stawka=stawka,
            wystawienie=wystawienie
        )
        db.session.add(faktura)
        db.session.commit()
        return "Faktura dodana. faktura id={}".format(faktura.id)
    except Exception as e:
	    return(str(e))

@app.route("/getall")
def get_all():
    try:
        faktury=Faktura.query.all()
        return  jsonify([f.serialize() for f in faktury])
    except Exception as e:
	    return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        faktura=Faktura.query.filter_by(id=id_).first()
        return jsonify(faktura.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/add/form",methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        numer=request.form.get('numer')
        stawka=request.form.get('stawka')
        wystawienie=request.form.get('wystawienie')
        try:
            faktura=Faktura(
                numer=numer,
                stawka=stawka,
                wystawienie=wystawienie
            )
            db.session.add(faktura)
            db.session.commit()
            return "Faktura dodana. faktura id={}".format(faktura.id)
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")

if __name__ == '__main__':
    app.run()
