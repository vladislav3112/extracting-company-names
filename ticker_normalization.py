from os import write
import csv
import numpy as np
import re
country_names = {' USA',' Australia',' China',' Spain'} #worth it or not?
stop_words = {' Class', ' Series', ' Depositary', ' Common', ' Ordinary Share',' Common Stock',' Warrant', ' Warrants',' Units', ' Unit',
                ' Co.',' Company',' Corp',' Inc.',' Ltd'} #TEMP

def ticker_is_primary(str):
    if (str.find('due') == -1 and str.find('Due') == -1 and len(str) < 80 and str.find(' Warrant') == -1 and str.find(' warrant') == -1 and str.find(' Right') == -1 and str.find('%') == -1):
        return True
    else:
        return False
special_chars ={'.',',','(',')',':','*','/',"'"}

def string_normalize(str):
    
    #step 0: remove 's
    str = str.replace("'s",'')

    #step 1: legal ang special charachter removal:
    str = ''.join(re. sub(r'\([^)]*\)', '', str))
    #step 2: case normalization
    str = str.title()
    #step xx: remove words that useless for matching
    for word in stop_words:
        str = str.partition(word)[0]
    #step 3: country name removal
    for name in country_names:
        str = str.replace(name,'')
    str = str.replace('Corporation','Corp')
    for char in special_chars:
        str = str.replace(char,'')
    if(str[-1]==' '):
        str = str[0:len(str)-1]
    return str

companies_list = []
nasdaq_dict = {}    #ticker - company
prev_str = ''
with open('company-tickers.txt', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        str = row[0].split(' ')
        ticker = str[0]
        del(str[0])
        str = ' '.join(str)
        if(ticker.find('^') == -1 and ticker_is_primary(str)):
            str = string_normalize(str)
            if(prev_str != str):
                nasdaq_dict[ticker] = str
                prev_str = str

with open('normalized tickers.txt','a',encoding='utf-8') as orgs_txt:
    for elem in nasdaq_dict:
        orgs_txt.write('\n')
        tmp = elem+' '+nasdaq_dict[elem]
        orgs_txt.write(tmp)