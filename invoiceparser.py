from itertools import islice
import re
import os
import jsonpickle
# import json
import nltk
from parsed_dict import ApiClient, Wyniki, Kwota, Stawka


keywords = ["sprzedawca", "strona", "nip", "oryginał", "kopia", "tel", "fax", "konto", "faktura", "nr", "nabywca",
            "data", "wystawienia", "sprzedaży", "towaru", "usługi", "ilość", "cena", "stawka", "netto", "vat",
            "wartość",
            "brutto", "należność", "ogółem", "formy", "płatności", "nip", "kwota"]


def datyParse(file):
    data_wystawienia = None
    data_sprzedazy = None

    for line in file:
        matches = re.search(r'\d{2}[:./-]\d{2}[:./-]\d{4}|\d{4}[:./-]\d{2}[:./-]\d{2}', line)
        if matches:
            for word in line.strip().lower().split():
                if nltk.edit_distance('wystawienia', word) < 4:
                    data_wystawienia = matches.group()
                elif nltk.edit_distance('sprzedaży', word) < 4:
                    data_sprzedazy = matches.group()
    return data_wystawienia, data_sprzedazy


def stawkaParse(file):
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
        matches = re.search(r'\d{3}-\d{3}-\d{2}-\d{2}|\d{3}-\d{2}-\d{2}-\d{3}|\d{10}', line)
        if matches and 'nip' in line.lower():
            nipy_org.append(matches.group())
            nipy.append(int(matches.group().replace('-', '')))
    nips = list(set(nipy))
    with open(r'C:\Users\Mateusz\flask-invoiceapp\Nip\nip.txt', 'w+') as h:
        if nips:
            for nip in nips:
                h.write(str(nip) + '\n')
    from runUiPath import checkNIP
    # TODO rozważyć case z nips[1]
    try:
        if not os.path.isfile(r'C:\Users\Mateusz\flask-invoiceapp\Nip\{}.txt'.format(str(nips[0]).strip())) or not os.path.isfile(r'C:\Users\Mateusz\flask-invoiceapp\Nip\{}.txt'.format(str(nips[1]).strip())):
            os.system(checkNIP)
    except IndexError:
        pass
    return nipy_org


def numerParse(file):
    flag = False
    flag2 = False
    numer_fv = None
    for line in file:
        match = re.search(r'faktura', line.lower())
        if match:
            for word in line.lower().split():
                if 'faktura' in word:
                    flag2 = True
                if flag2:
                    if word[0].isdigit():
                        if not flag:
                            numer_fv = word.replace(',', '')
                            flag = True
    return numer_fv


def nabywca(file):
    nipy = nipParse(file)
    wersy = []
    dane_firmy = []
    indeks_nabywcy = None
    for np in nipy:
        path = "C:\\Users\\Mateusz\\Documents\\UiPath\\Nip\\{}.txt".format(str(np))
        with open(path, 'r', encoding='utf8') as plik:
            for line0 in plik.readlines():
                dane_firmy.append(line0.lower().strip())
            for line in file:
                wersy.append(line.strip().lower())
                if dane_firmy[0] in line.lower():
                    firma = line.lower().strip()
        for item in wersy:
            if 'nabywca' in item:
                indeks_nabywcy = wersy.index(item)
        indeks_firmy = wersy.index(firma)
        if abs(indeks_nabywcy - indeks_firmy) < 2:
            print({'nabywca': firma})
        for i in range(indeks_firmy - 2, indeks_firmy + 2):
            if dane_firmy[1] in wersy[i]:
                print({'ulica_nabywcy': dane_firmy[1]})
            if dane_firmy[2] in wersy[i]:
                print({'kod_nabywcy': dane_firmy[2]})
            if dane_firmy[3] in wersy[i]:
                print({'miasto_nabywcy': dane_firmy[3]})


def sprzedawca(file):
    wersy = []
    dane_firmy = []
    indeks_sprzedawcy = None
    with open(r'C:\Users\Mateusz\flask-invoiceapp\Nip\5220001116.txt', 'r', encoding='utf8') as plik:
        for line0 in plik.readlines():
            dane_firmy.append(line0.lower().strip())
        for line in file:
            wersy.append(line.strip().lower())
            if dane_firmy[0].replace(' ', '') in line.strip().lower().replace(' ', '') or line.strip().lower()[:-1].replace(' ', '') in dane_firmy[0].replace(' ', ''):
                firma = line.lower().strip()
            elif dane_firmy[0].replace(' ', '') in line.strip().lower().replace(' ', ''):
                firma = line.lower().strip()
    for item in wersy:
        if 'sprzedawca' in item:
            indeks_sprzedawcy = wersy.index(item)
    indeks_firmy = wersy.index(firma)
    if abs(indeks_sprzedawcy - indeks_firmy) < 2:
        print({'sprzedawca': firma})
    for i in range(indeks_firmy - 2, indeks_firmy + 2):
        if dane_firmy[1] in wersy[i]:
            print({'ulica_sprzedawcy': dane_firmy[1]})
        if dane_firmy[2] in wersy[i]:
            print({'kod_sprzedawcy': dane_firmy[2]})
        if dane_firmy[3] in wersy[i]:
            print({'miasto_sprzedawcy': dane_firmy[3]})


def data(file):
    slowa = []
    dates = []
    pary = []
    wynik = None
    indeks_wystawienia = None
    for line in file:
        for word in line.split():
            slowa.append(word.strip().lower())
            match = re.search(r'\d{4}-\d{2}-\d{2}', word)
            if match:
                dates.append(match.group())
            else:
                match = re.search(r'\d{2}/\d{2}/\d{4}', word)
                if match:
                    dates.append(match.group())

    for slowo in slowa:
        if 'wystawienia' in slowo.lower().strip():
            indeks_wystawienia = slowa.index(slowo)
    for dat in dates:
        para = (abs(slowa.index(dat) - indeks_wystawienia), dat)
        pary.append(para)
    minimums = []
    for krotka in pary:
        minimums.append(krotka[0])
    minimum = min(minimums)
    for krotka in pary:
        if krotka[0] == minimum:
            wynik = krotka[1]
    return wynik


def integery(file):
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
                # else:
                #     liczby_calkowite.append(int(word.strip().lower()))
                #     liczby_calkowite_str.append(word.strip().lower())
            except ValueError:
                continue
    import collections
    # print(slowa)
    koncowki_kwot = [item for item, count in collections.Counter(liczby_calkowite_str).items() if count > 1]
    koncowki_kwot_float = [item for item, count in collections.Counter(liczby_calkowite).items() if count > 1]
    # print(slowa.index(koncowki_kwot[0]))
    # print(slowa.index(koncowki_kwot[1]))
    # print(slowa.index(koncowki_kwot[2]))


    def list_duplicates_of(seq, item):
        start_at = -1
        locs = []
        while True:
            try:
                loc = seq.index(item, start_at + 1)
            except ValueError:
                break
            else:
                locs.append(loc)
                start_at = loc
        return locs

    # print(list_duplicates_of(slowa, koncowki_kwot[0]))
    # print(list_duplicates_of(slowa, koncowki_kwot[1]))
    # print(list_duplicates_of(slowa, koncowki_kwot[2]))
    brutto = list_duplicates_of(slowa, koncowki_kwot[2])
    # print(slowa[102:105])
    print(koncowki_kwot)
    for i in range(3):
        match2 = re.search(r',\d{2}', slowa[brutto[0]-i])
        if not match2:
            print(slowa[brutto[0]-i+1:brutto[0]+1])
    # # liczby_calkowite_str.remove('5252690805')
    # # liczby_calkowite_str.remove('5221009522')
    # # print(liczby_calkowite_str)
    # import collections
    # # print([item for item, count in collections.Counter(liczby_calkowite_str).items() if count > 1])
    # listaduplikatow = [item for item, count in collections.Counter(liczby_calkowite_str).items() if count > 1]
    # skonkatenowany = ''.join(liczby_calkowite_str)
    # # print(''.join(liczby_calkowite_str))
    # # for e in listaduplikatow:
    # for i in range(5):
    #     if ''.join(listaduplikatow[0:i]) in skonkatenowany:
    #         a = 1
    #     else:
    #         a = 2
    #     if a == 2:
    #         print(''.join(listaduplikatow[0:i-1]))
    #

    if float(max(koncowki_kwot_float)) - float(min(koncowki_kwot_float)) in koncowki_kwot_float:
        brutto = float(max(koncowki_kwot_float))
        netto = float(max(koncowki_kwot_float)) - float(min(koncowki_kwot_float))
        vat = float(min(koncowki_kwot_float))
        print({'brutto': brutto, 'netto': netto, 'vat': vat})


def dane_z_wyszukiwarki(identyfikator):
    dane_firmy = []
    dane_firmy_surowe = []
    try:
        # with open(r'C:\Users\Mateusz\Documents\UiPath\Nip\{}.txt'.format(identyfikator), 'r', encoding='utf8') as plik:
        with open(r'C:\Users\Mateusz\flask-invoiceapp\Nip\{}.txt'.format(identyfikator), 'r', encoding='utf8') as plik:
            for line0 in plik.readlines():
                dane_firmy_surowe.append(line0.strip())
                dane_firmy.append(line0.lower().strip().replace(' ', ''))
        return dane_firmy_surowe
    except FileNotFoundError:
        return ["Nie znaleziono danych firmy po nipie"]


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

        indeks_nip_sprzedawcy = indeks_sprzedawcy + min(abs(indeks_sprzedawcy-indeks_nipu_0), abs(indeks_sprzedawcy-indeks_nipu_1))
        indeks_nip_nabywcy = indeks_nabywcy + min(abs(indeks_nabywcy - indeks_nipu_0), abs(indeks_nabywcy - indeks_nipu_1))
        if indeks_nip_sprzedawcy == indeks_nipu_0:
            nip_sprzedawcy = nipy[0]
        else:
            nip_sprzedawcy = nipy[1]

        if indeks_nip_nabywcy == indeks_nipu_0:
            nip_nabywcy = nipy[0]
        else:
            nip_nabywcy = nipy[1]
        # print(int(nip_sprzedawcy.replace('-', '')), int(nip_nabywcy.replace('-','')))
        print(nip_sprzedawcy, nip_nabywcy)
    elif len(nipy) == 1:
        nip_sprzedawcy = nipy[0]
        dane_sprzedawcy = dane_z_wyszukiwarki(nip_sprzedawcy.replace('-', ''))
        dane_sprzedawcy.append(nip_sprzedawcy.replace('-', ''))
        return {"sprzedawca": dane_sprzedawcy, "nabywca": None}

    if nip_sprzedawcy is not None and nip_nabywcy is not None:
        dane_sprzedawcy = dane_z_wyszukiwarki(nip_sprzedawcy.replace('-', ''))
        dane_nabywcy = dane_z_wyszukiwarki(nip_nabywcy.replace('-', ''))
        dane_sprzedawcy.append(nip_sprzedawcy.replace('-', ''))
        dane_nabywcy.append(nip_nabywcy.replace('-', ''))
        return {"sprzedawca": dane_sprzedawcy, "nabywca": dane_nabywcy}


def wypelnienie(file):
    os.makedirs(os.path.dirname('parsed_successful/'), exist_ok=True)

    wynik = Wyniki()
    wynik.data_wystawienia, wynik.data_sprzedazy = datyParse(file)
    wynik.numer = numerParse(file)

    stawka = Stawka()
    stawka.stawka = stawkaParse(file)[0]
    stawka.zgodna = stawkaParse(file)[1]
    wynik.stawka = stawka

    kurwa_sprzedajacy = podmiot_z_nipu(file)
    wynik.sprzedawca = '\n'.join(kurwa_sprzedajacy["sprzedawca"])

    if kurwa_sprzedajacy["nabywca"]:
        wynik.nabywca = '\n'.join(kurwa_sprzedajacy["nabywca"])
    else:
        wynik.nabywca = dostawcakurwa(file)

    kwota = Kwota()
    kwota.brutto = '675'
    kwota.netto = '625'
    kwota.vat = '50'
    kwota.waluta = 'PLN'
    wynik.kwota = kwota

    apiclient = ApiClient()
    writeRes = jsonpickle.encode(apiclient.sanitize_for_serialization(wynik), unpicklable=False)
    writeRes = writeRes.encode('utf-8')

    with open('parsed_successful/' + str(wynik.numer).replace('/', '') + '.json', 'wb') as g:
        g.write(writeRes)
    return wynik


def dostawcakurwa(file):
    nabywca = None
    for idx, line in enumerate(file):
        if 'nabywca' in line.lower():
            nabywca = ''.join(islice(file, idx, idx + 4))
    print(nabywca)
    return nabywca
