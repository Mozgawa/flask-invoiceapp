# import jsonpickle
import re
import os
import collections
import nltk
from itertools import islice
from .parsed_object import Wyniki  # , ApiClient
from .UiPath_robots.robot_paths import checkNIP


def numberParse(file):
    flag = False
    numer = None
    threshold = 0.57

    for line in file:
        for word in line.lower().split():
            if flag:
                if word[0].isdigit() or sum(c.isdigit() for c in word) / len(word.replace('/', '')) > threshold:
                    numer = word.replace(',', '')
                    break
            else:
                if nltk.edit_distance('faktura', word) < 4:
                    flag = True
        if numer:
            break
    return numer


def datesParse(file):
    data_wystawienia = None
    data_sprzedazy = None

    for line in file:
        matches = re.search(r'\d{2}[:./-]\d{2}[:./-]\d{4}|\d{4}[:./-]\d{2}[:./-]\d{2}', line)
        if matches:
            for word in line.strip().lower().split():
                if nltk.edit_distance('wystawienia', word) < 4:
                    data_wystawienia = matches.group()
                elif nltk.edit_distance('sprzedazy', word) < 4:
                    data_sprzedazy = matches.group()
    return data_wystawienia, data_sprzedazy


def stakeParse(file):
    match = None
    zgodna = None
    mozliwe_stawki = ['23%', '8%', '5%', '0%']
    for line in file:
        if '%' in line:
            matches = re.search(r'\d{1,2}%', line)
            if matches:
                match = str(matches.group())
    if match in mozliwe_stawki:
        zgodna = True
    return match, zgodna


def nipParse(file):
    nipy = []
    nipy_org = []
    for line in file:
        matches = re.findall(r'\d{3}-\d{3}-\d{2}-\d{2}|\d{3}-\d{2}-\d{2}-\d{3}|\d{10}', line)
        if matches and 'nip' in line.lower():
            for match in matches:
                nipy_org.append(match)
                nipy.append(int(match.replace('-', '')))
    nips = list(set(nipy))
    with open(r'C:\Users\Mateusz\flask-invoiceapp\invoice_parser\UiPath_robots\NIP\nip.txt', 'w+') as h:
        if nips:
            for nip in nips:
                h.write(str(nip) + '\n')
    try:
        if not os.path.isfile(r'C:\Users\Mateusz\flask-invoiceapp\invoice_parser\UiPath_robots\NIP\{}.txt'.format(
                str(nips[0]).strip())) or \
                not os.path.isfile(r'C:\Users\Mateusz\flask-invoiceapp\invoice_parser\UiPath_robots\NIP\{}.txt'.format(
                    str(nips[1]).strip())):
            os.system(checkNIP)
    except IndexError:
        pass
    return nipy_org


def amountParse(file):
    liczby_calkowite = []
    liczby_calkowite_str = []
    slowa = []
    for line in file:
        for word in line.split():
            slowa.append(word.strip().lower())
            match = re.search(r',\d{2}', word)
            try:
                if match:
                    liczby_calkowite.append(float(word.strip().lower().replace(',', '.')))
                    liczby_calkowite_str.append(word.strip().lower())
            except ValueError:
                continue
    koncowki_kwot = [item for item, count in collections.Counter(liczby_calkowite_str).items() if count > 1]
    if koncowki_kwot:
        return max(koncowki_kwot)


def dane_z_wyszukiwarki(identyfikator):
    dane_firmy = []
    dane_firmy_surowe = []
    try:
        with open(r'C:\Users\Mateusz\flask-invoiceapp\invoice_parser\UiPath_robots\NIP\{}.txt'.format(identyfikator), 'r', encoding='utf8') as file:
            for line in file.readlines():
                dane_firmy_surowe.append(line.strip())
                dane_firmy.append(line.lower().strip().replace(' ', ''))
        return dane_firmy_surowe
    except FileNotFoundError:
        print("Nie znaleziono danych firmy po nipie!")
        return None


def podmiot_z_nipu(file):
    nipy = nipParse(file)
    indeks_sprzedawcy = None
    indeks_nabywcy = None
    indeks_nipu_0 = None
    indeks_nipu_1 = None
    nip_sprzedawcy = None
    nip_nabywcy = None
    if len(nipy) > 1:
        for nr, element in enumerate(file):
            if "sprzedawca" in element.lower():
                indeks_sprzedawcy = nr
            if "nabywca" in element.lower():
                indeks_nabywcy = nr
            if nipy[0] in element.lower():
                indeks_nipu_0 = nr
            if nipy[1] in element.lower():
                indeks_nipu_1 = nr
        indeks_nip_sprzedawcy = indeks_sprzedawcy + min(abs(indeks_sprzedawcy - indeks_nipu_0),
                                                        abs(indeks_sprzedawcy - indeks_nipu_1))
        indeks_nip_nabywcy = indeks_nabywcy + min(abs(indeks_nabywcy - indeks_nipu_0),
                                                  abs(indeks_nabywcy - indeks_nipu_1))
        if indeks_nip_sprzedawcy == indeks_nipu_0:
            nip_sprzedawcy = nipy[0]
        else:
            nip_sprzedawcy = nipy[1]

        if indeks_nip_nabywcy == indeks_nipu_0:
            nip_nabywcy = nipy[0]
        else:
            nip_nabywcy = nipy[1]

        if nip_nabywcy == nip_sprzedawcy:
            nip_sprzedawcy = nipy[1]
            if nip_nabywcy == nip_sprzedawcy:
                nip_sprzedawcy = nipy[0]
    elif len(nipy) == 1:
        nip_sprzedawcy = nipy[0]
        dane_sprzedawcy = dane_z_wyszukiwarki(nip_sprzedawcy.replace('-', ''))
        dane_sprzedawcy.append(nip_sprzedawcy.replace('-', ''))
        return {"sprzedawca": dane_sprzedawcy, "nabywca": None}
    if nip_sprzedawcy is not None and nip_nabywcy is not None:
        dane_sprzedawcy = dane_z_wyszukiwarki(nip_sprzedawcy.replace('-', ''))
        dane_nabywcy = dane_z_wyszukiwarki(nip_nabywcy.replace('-', ''))
        try:
            dane_sprzedawcy.append(nip_sprzedawcy.replace('-', ''))
        except AttributeError:
            dane_sprzedawcy = None
        try:
            dane_nabywcy.append(nip_nabywcy.replace('-', ''))
        except AttributeError:
            dane_nabywcy = None
        return {"sprzedawca": dane_sprzedawcy, "nabywca": dane_nabywcy}


def dostawca_z_ocr(file):
    nabywca = None
    for idx, line in enumerate(file):
        if 'nabywca' in line.lower():
            nabywca = ''.join(islice(file, idx, idx + 4))
    return nabywca


def sprzedawca_z_ocr(file):
    sprzedawca = None
    for idx, line in enumerate(file):
        if 'sprzedawca' in line.lower():
            sprzedawca = ''.join(islice(file, idx, idx + 4))
    return sprzedawca


def filling(file):
    # os.makedirs(os.path.dirname('parsed_successful/'), exist_ok=True)

    wynik = Wyniki()
    wynik.data_wystawienia, wynik.data_sprzedazy = datesParse(file)
    wynik.numer = numberParse(file)
    wynik.stawka = stakeParse(file)[0]
    wynik.kwota = amountParse(file)

    kurwa_sprzedajacy = podmiot_z_nipu(file)
    if kurwa_sprzedajacy['sprzedawca']:
        wynik.sprzedawca = '\n'.join(kurwa_sprzedajacy["sprzedawca"])
    else:
        wynik.sprzedawca = sprzedawca_z_ocr(file)

    if kurwa_sprzedajacy["nabywca"]:
        wynik.nabywca = '\n'.join(kurwa_sprzedajacy["nabywca"])
    else:
        wynik.nabywca = dostawca_z_ocr(file)

    # apiclient = ApiClient()
    # writeRes = jsonpickle.encode(apiclient.sanitize_for_serialization(wynik), unpicklable=False)
    # writeRes = writeRes.encode('utf-8')

    # with open('parsed_successful/' + str(wynik.numer).replace('/', '') + '.json', 'wb') as g:
    #     g.write(writeRes)
    return wynik
