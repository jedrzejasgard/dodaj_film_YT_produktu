import configparser
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep


config = configparser.ConfigParser()
config.read('settings.ini')

l = config.get('evolve', 'user')
had = config.get('evolve', 'pass')

evolve_url = 'https://asgard.gifts/admin/'
lista_produktow_url = 'https://asgard.gifts/admin/productList/0/'
chrome = webdriver.Chrome(
    r'C:\Users\asgard_48\Documents\chromedriver_win32\chromedriver.exe')
chrome.get(evolve_url)
chrome.maximize_window()
chrome.find_element_by_name('uLogin').send_keys(l)
chrome.find_element_by_name('uPasswd').send_keys(had)
chrome.find_element_by_xpath(
    '/html/body/div[2]/div[1]/form/button').click()
chrome.get(lista_produktow_url)
sleep(1)
chrome.close()
