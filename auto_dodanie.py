import configparser
from vendoasg.vendoasg import Vendo
import pandas as pd
from os.path import exists
import sys
import json

config = configparser.ConfigParser()
config.read('settings.ini')

l = config.get('evolve', 'user')
had = config.get('evolve', 'pass')
path = r'C:\\Users\\asgard_48\\Documents\\Skrypty\\dodaj_filmy_YT_F5\\'

# ************ nazwa pliku do wgrania **************
nPlik = input('Wpisz nazwę pliku do wgrania:  ')
#formatPliku = input('Wpisz format pliku do wgrania (xls/xlsx):  ')
pelna_nazwa_pliku = None
if exists(f'{path}{nPlik}.xls'):
    pelna_nazwa_pliku = f'{nPlik}.xls'
elif exists(f'{path}{nPlik}.xlsx'):
    pelna_nazwa_pliku = f'{nPlik}.xlsx'
else:
    print('Nie znalazlem pliku')
    sys.exit()


def lista_kodow(kod_towaru):
    # pobiera z Vendo możliwe wersje kolorystyczne koloru i zwraca listę
    kolory_produktu = []
    response_data = vendoApi.getJson(
        '/json/reply/Magazyn_Towary_Towary',
        {"Token": vendoApi.USER_TOKEN, "Model": {"Kod": kod_towaru}}
    )
    response_data = response_data["Wynik"]["Rekordy"]
    for produkt in response_data:
        kolory_produktu.append(produkt["Kod"])
    return kolory_produktu


with open(f"{pelna_nazwa_pliku}", 'rb')as tabelaDane:
    plik = pd.read_excel(tabelaDane).dropna()
    plik.drop(index=plik.index[0],
              axis=0,
              inplace=True)

# połączenie z bazą vendo
vendoApi = Vendo(config.get('vendo', 'vendo_API_port'))
vendoApi.logInApi(config.get('vendo', 'logInApi_user'),
                  config.get('vendo', 'logInApi_pass'))
vendoApi.loginUser(config.get('vendo', 'loginUser_user'),
                   config.get('vendo', 'loginUser_pass'))

# Utworzenie dict dla każdego produktu i przypisanie mu linku yutube do dopowiedniej wersji jezykowej
dict_produktow = {}

for index, row in plik.iterrows():
    index_prod = row[1]
    link_yt = row[2].replace('youtu.be/', 'youtube.com/watch?v=')
    jezyk = row[0].split(' ')[-1]
    

    print(jezyk)
    if jezyk.lower() == 'pl':
        dict_produktow[index_prod] ={}
        dict_produktow[index_prod]['PL'] = link_yt
    elif jezyk.lower() == 'en':
        dict_produktow[index_prod]['EN'] = link_yt
    elif jezyk.lower() == 'de':
        dict_produktow[index_prod]['DE'] = link_yt
    elif jezyk.lower() == 'fr':
        dict_produktow[index_prod]['FR'] = link_yt

# wgranie dla każdej wersji kolorystycznej produktu dict z linkami filmów
for index_prod in dict_produktow:
    print(index_prod)
    kolory_produktu = lista_kodow(index_prod)
    print(kolory_produktu)
    for wariant_kolorystyczny in kolory_produktu:
        kod_query = vendoApi.getJson(
            '/Magazyn/Towary/Towar', {"Token": vendoApi.USER_TOKEN, "Model": {"Towar": {"Kod": wariant_kolorystyczny}}})

        numerID = kod_query["Wynik"]["Towar"]["ID"]
        wartosc_do_wgrania = json.dumps(dict_produktow[index_prod])
        #print(wartosc_do_wgrania[1:-1].replace('"','').replace(',',';'))
        response_data = vendoApi.getJson('/json/reply/Magazyn_Towary_Aktualizuj', {"Token": vendoApi.USER_TOKEN, "Model": {
                                         "ID": numerID, "PolaUzytkownika": {"NazwaWewnetrzna": 'towar_film_YT', "Wartosc": wartosc_do_wgrania}}})
        print(response_data)
        print(f"Dodaję KOD: {index_prod} wartość: {wartosc_do_wgrania}")
print(dict_produktow)
sys.exit()
