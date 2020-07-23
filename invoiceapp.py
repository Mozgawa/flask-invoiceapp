# import os
from flask import jsonify  # Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
# import pandas as pd
from tables import Results

import os
# import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from parsowacz2 import wypelnienie


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
    try:
        faktura = Faktura(
            numer=numer,
            stawka=stawka,
            wystawienie=wystawienie
        )
        db.session.add(faktura)
        db.session.commit()
        return "Faktura dodana. faktura id={}".format(faktura.id)
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


@app.route("/add/form", methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        numer = request.form.get('numer')
        stawka = request.form.get('stawka')
        wystawienie = request.form.get('wystawienie')
        try:
            faktura = Faktura(
                numer=numer,
                stawka=stawka,
                wystawienie=wystawienie
            )
            db.session.add(faktura)
            db.session.commit()
            return "Faktura dodana. faktura id={}".format(faktura.id)
        except Exception as e:
            return str(e)
    # return render_template("getdata.html")
    return render_template("getdata.html")


@app.route('/results')
def search_results():
    # results = []
    # search_string = search.data['search']
    # if search.data['search'] == '':
    results = Faktura.query.all()
    # if not results:
    #     flash('No results found!')
    #     return redirect('/')
    # else:
    #     # display results
    #     table = Results(results)
    #     table.border = True
    table = Results(results)
    table.border = True
    return render_template('result.html', table=table)


# import os
# import urllib.request
# from flask import Flask, flash, request, redirect, url_for, render_template
# from werkzeug.utils import secure_filename

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
        # print('upload_image filename: ' + filename)
        # flash('Image successfully uploaded and displayed')
        # faktury = Faktura.query.all()
        # print(jsonify([f.serialize() for f in faktury]).json())
        # g = open('invoice_ocr.txt', 'r', encoding='utf8')
        # g = open('C:\\Users\\Mateusz\\Documents\\UiPath\\InvoiceOCR\\ocr_text.txt', 'r', encoding='utf8')
        g = open('C:\\Users\\Mateusz\\flask-invoiceapp\\InvoiceOCR\\ocr_text.txt', 'r', encoding='utf8')
        wynik = wypelnienie(g.readlines())
        # flash(wypelnienie(g.readlines()))
        g.close()
        # flash(str([f.serialize() for f in faktury]))
        return render_template('upload.html', filename=filename, numer=str(wynik.numer), nazwa=str(wynik.nabywca.nazwa) + "\n" + str(wynik.nabywca.adres.ulica) + "\n" + str(wynik.nabywca.adres.kod_pocztowy) + " " + str(wynik.nabywca.adres.miejscowosc) + "\n" + "NIP:" + str(wynik.nabywca.nip), sprzedawca=str(wynik.sprzedawca.nazwa) + "\n" + str(wynik.sprzedawca.adres.ulica) + "\n" + str(wynik.sprzedawca.adres.kod_pocztowy) + " " + str(wynik.sprzedawca.adres.miejscowosc) + "\n" + "NIP:" + str(wynik.sprzedawca.nip), value=str(wynik.nabywca.nip), data_wystawienia=wynik.data_wystawienia)
        # return render_template('upload.html', filename="brightened-image.png", numer=str(wynik.numer), nazwa=str(wynik.nabywca.nazwa) + "\n" + str(wynik.nabywca.adres.ulica) + "\n" + str(wynik.nabywca.adres.kod_pocztowy) + " " + str(wynik.nabywca.adres.miejscowosc) + "\n" + "NIP:" + str(wynik.nabywca.nip), sprzedawca=str(wynik.sprzedawca.nazwa) + "\n" + str(wynik.sprzedawca.adres.ulica) + "\n" + str(wynik.sprzedawca.adres.kod_pocztowy) + " " + str(wynik.sprzedawca.adres.miejscowosc) + "\n" + "NIP:" + str(wynik.sprzedawca.nip), value=str(wynik.nabywca.nip), data_wystawienia=wynik.data_wystawienia)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.run()
