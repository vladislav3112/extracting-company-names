from os import write
import csv
import numpy as np
import re
country_names = {'USA','Australia','China','Spain','Canada'}
stop_words = {'Shares', 'Co', 'Inc','Stock', 'Trust','Warrant','Unit', 'Fund'}
companies_list = []
nasdaq_dict = {}    #ticker - company

def string_normalize(str):
    #step 1: legal ang special charachter removal:
    str = ''.join(re.split(r'(?:[()])',str))
    #step 2: case normalization
    #step 3: country name removal
    for name in country_names:
        str = str.replace(name,'')
    return str

with open('company-tickers.txt', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        str = row[0].split(' ')
        ticker = str[0]
        del(str[0])
        str = ' '.join(str)
        str = string_normalize(str)
        if(ticker.find('^') == -1 and ticker.find('due')!=-1 and ticker.find('Due')):
            nasdaq_dict[ticker] = str
with open('normalized tickers.txt','a',encoding='utf-8') as orgs_txt:
    for elem in nasdaq_dict:
        orgs_txt.write('\n')
        tmp = elem+' '+nasdaq_dict[elem]
        orgs_txt.write(tmp)