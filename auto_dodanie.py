import configparser
from vendoasg.vendoasg import Vendo
import pandas as pd
from time import sleep
from os.path import exists
import sys
import re

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

with open(f"{pelna_nazwa_pliku}", 'rb')as tabelaDane:
    plik = pd.read_excel(tabelaDane, usecols=['Unnamed: 1','Unnamed: 2']).dropna()
    plik.drop(index=plik.index[0], 
        axis=0, 
        inplace=True)
print(plik)

# połączenie z bazą vendo
vendoApi = Vendo(config.get('vendo', 'vendo_API_port'))
vendoApi.logInApi(config.get('vendo', 'logInApi_user'),
                  config.get('vendo', 'logInApi_pass'))
vendoApi.loginUser(config.get('vendo', 'loginUser_user'),
                   config.get('vendo', 'loginUser_pass'))

for index, row in plik.iterrows():
    index_prod = row[0]
    link_yt = row[1].replace('youtu.be/','youtube.com/watch?v=')
    print(link_yt)

sys.exit()
