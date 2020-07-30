import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from tables import Results
from invoiceparser import wypelnienie


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Faktura


@app.route("/add")
def add_book():
    numer = request.args.get('numer')
    stawka = request.args.get('stawka')
    wystawienie = request.args.get('wystawienie')
    sprzedaz = request.args.get('sprzedaz')
    kwota = request.args.get('kwota')
    sprzedawca = request.args.get('sprzedawca')
    nabywca = request.args.get('nabywca')

    try:
        faktura = Faktura(
            numer=numer,
            stawka=stawka,
            wystawienie=wystawienie,
            sprzedaz=sprzedaz,
            kwota=kwota,
            sprzedawca=sprzedawca,
            nabywca=nabywca
        )
        db.session.add(faktura)
        db.session.commit()
        # return "Faktura dodana. faktura id={}".format(faktura.id)
        return redirect('/results')
    except Exception as e:
        return str(e)


@app.route("/getall")
def get_all():
    try:
        faktury = Faktura.query.all()
        return jsonify([f.serialize() for f in faktury])
    except Exception as e:
        return str(e)


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        faktura = Faktura.query.filter_by(id=id_).first()
        return jsonify(faktura.serialize())
    except Exception as e:
        return str(e)


@app.route('/results')
def search_results():
    results = Faktura.query.all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        table = Results(results)
        table.border = True
    return render_template('result.html', table=table)


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        from scanning import scan
        scan(filename)
        from runUiPath import extractText
        os.system(extractText)
        g = open('C:\\Users\\Mateusz\\flask-invoiceapp\\InvoiceOCR\\ocr_text.txt', 'r', encoding='utf8')
        wynik = wypelnienie(g.readlines())
        g.close()
        if not wynik.data_wystawienia and wynik.data_sprzedazy:
            wynik.data_wystawienia = wynik.data_sprzedazy
        return render_template('upload.html', filename=filename, numer=str(wynik.numer), nazwa=str(wynik.nabywca), sprzedawca=str(wynik.sprzedawca), data_wystawienia=wynik.data_wystawienia, data_sprzedazy=wynik.data_sprzedazy, stawka=str(wynik.stawka.stawka), kwota=str(wynik.kwota.brutto))
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.run()
