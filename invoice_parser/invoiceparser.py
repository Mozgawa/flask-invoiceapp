import re
import os
import collections
import nltk
from itertools import islice
from .UiPath_robots.robot_paths import checkNIP

path = r'C:/Users\Mateusz/flask-invoiceapp/invoice_parser/UiPath_robots/NIP/'


def generalParser(file):
    number = None
    stake = None
    amount = None
    issue_date = None
    sale_date = None
    flag = False
    threshold = 0.57
    integers_as_strings = []
    integers = []
    words = []

    for line in file:

        if not stake:
            if '%' in line:
                matches = re.search(r'\d{1,2}%', line)
                if matches:
                    stake = str(matches.group())

        if not issue_date or not sale_date:
            matches2 = re.search(r'\d{2}[:./-]\d{2}[:./-]\d{4}|\d{4}[:./-]\d{2}[:./-]\d{2}', line)
            if matches2:
                for word in line.strip().lower().split():
                    if nltk.edit_distance('wystawienia', word) < 4:
                        issue_date = matches2.group()
                    elif nltk.edit_distance('sprzedazy', word) < 4:
                        sale_date = matches2.group()

        if not number:
            for word in line.lower().split():
                if flag:
                    try:
                        if word[0].isdigit() or sum(c.isdigit() for c in word) / len(word.replace('/', '')) > threshold:
                            number = word.replace(',', '')
                    except ZeroDivisionError:
                        continue
                else:
                    if nltk.edit_distance('faktura', word) < 4:
                        flag = True

        for word in line.split():
            words.append(word.strip().lower())
            match = re.search(r',\d{2}', word)
            try:
                if match:
                    integers.append(float(word.strip().lower().replace(',', '.')))
                    integers_as_strings.append(word.strip().lower())
            except ValueError:
                continue

    ending_amounts = [item for item, count in collections.Counter(integers_as_strings).items() if count > 1]
    if ending_amounts:
        amount = max(ending_amounts)

    return {"number": number, "issue_date": issue_date, "sale_date": sale_date, "stake": stake, "amount": amount}


def nipParse(file):
    nips = []
    nips_org = []
    for line in file:
        matches = re.findall(r'\d{3}-\d{3}-\d{2}-\d{2}|\d{3}-\d{2}-\d{2}-\d{3}|\d{10}', line)
        if matches and 'nip' in line.lower():
            for match in matches:
                nips_org.append(match)
                nips.append(int(match.replace('-', '')))
    nips = list(set(nips))
    with open(f'{path}nip.txt', 'w+') as f:
        if nips:
            for nip in nips:
                f.write(str(nip) + '\n')
    try:
        if not os.path.isfile(f'{path}{str(nips[0]).strip()}.txt') or not os.path.isfile(f'{path}{str(nips[1]).strip()}.txt'):
            os.system(checkNIP)
    except IndexError:
        pass
    return nips_org


def dataGUS(tax_id):
    company_data = []
    company_raw_data = []
    try:
        with open(f'{path}{tax_id}.txt', 'r', encoding='utf8') as file:
            for line in file.readlines():
                company_raw_data.append(line.strip())
                company_data.append(line.lower().strip().replace(' ', ''))
        return company_raw_data
    except FileNotFoundError:
        print(f"Nie znaleziono danych firmy po nipie: {tax_id}!")
        return None


def entityGUS(file):
    nips = nipParse(file)
    sellex_idx = None
    buyer_idx = None
    nip0_idx = None
    nip1_idx = None
    seller_nip = None
    buyer_nip = None
    if len(nips) > 1:
        for nr, element in enumerate(file):
            if "sprzedawca" in element.lower():
                sellex_idx = nr
            if "nabywca" in element.lower():
                buyer_idx = nr
            if nips[0] in element.lower():
                nip0_idx = nr
            if nips[1] in element.lower():
                nip1_idx = nr
        try:
            seller_nip_idx = sellex_idx + min(abs(sellex_idx - nip0_idx), abs(sellex_idx - nip1_idx))
        except TypeError:
            seller_nip_idx = None
        try:
            buyer_nip_idx = buyer_idx + min(abs(buyer_idx - nip0_idx), abs(buyer_idx - nip1_idx))
        except TypeError:
            buyer_nip_idx = None

        if seller_nip_idx == nip0_idx:
            seller_nip = nips[0]
        else:
            seller_nip = nips[1]

        if buyer_nip_idx == nip0_idx:
            buyer_nip = nips[0]
        else:
            buyer_nip = nips[1]

        if buyer_nip == seller_nip:
            seller_nip = nips[1]
            if buyer_nip == seller_nip:
                seller_nip = nips[0]
    elif len(nips) == 1:
        seller_nip = nips[0]
        seller_data = dataGUS(seller_nip.replace('-', ''))
        seller_data.append(seller_nip.replace('-', ''))
        return {"sprzedawca": seller_data, "nabywca": None}
    if seller_nip is not None and buyer_nip is not None:
        seller_data = dataGUS(seller_nip.replace('-', ''))
        buyer_data = dataGUS(buyer_nip.replace('-', ''))
        try:
            seller_data.append(seller_nip.replace('-', ''))
        except AttributeError:
            seller_data = None
        try:
            buyer_data.append(buyer_nip.replace('-', ''))
        except AttributeError:
            buyer_data = None
        return {"seller": seller_data, "buyer": buyer_data}
    else:
        return {"sprzedawca": None, "nabywca": None}


def buyerOCR(file):
    nabywca = None
    for idx, line in enumerate(file):
        if 'nabywca' in line.lower():
            nabywca = ''.join(islice(file, idx, idx + 4))
    return nabywca


def sellerOCR(file):
    sprzedawca = None
    for idx, line in enumerate(file):
        if 'sprzedawca' in line.lower():
            sprzedawca = ''.join(islice(file, idx, idx + 4))
    return sprzedawca


def filling(file, invoice):
    result = generalParser(file)
    entity = entityGUS(file)
    return invoice(
        numer=result.get("number"),
        kwota=result.get("amount"),
        stawka=result.get("stake"),
        sprzedaz=result.get("sale_date"),
        wystawienie=result.get("issue_date"),
        sprzedawca='\n'.join(entity.get("seller")) if entity.get("seller") else sellerOCR(file),
        nabywca='\n'.join(entity.get("buyer")) if entity.get("buyer") else buyerOCR(file)
    )
