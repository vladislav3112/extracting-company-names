from os import write
import csv
import pandas as pd
import re
country_names = {' USA',' Australia',' China',' Spain'} #worth it or not?
stop_words = {' Class', ' Series', ' Depositary', ' Common', ' Ordinary Share',' Common Stock',' Warrant', ' Warrants',' Units', ' Unit',
                ' Co.',' Company',' Corp',' Inc.',' Ltd'} #TEMP

def ticker_is_primary(str):
    if (str.find(' due') == -1 and str.find(' Due') == -1 and len(str) < 80 and str.find(' Warrant') == -1 and str.find(' warrant') == -1 and str.find(' Right') == -1 and str.find('%') == -1):
        return True
    else:
        return False
special_chars ={'.',',','(',')',':','*','/',"'","&"}

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

df_tickers = pd.read_csv('company-tickers.csv',index_col=False,header=0)
names = df_tickers['Name']
tickers = df_tickers['Symbol'] 
df_tickers = df_tickers[df_tickers.Symbol.str.find('^')==-1]
df_tickers = df_tickers[df_tickers.Symbol.str.len() < 5]
ticker_indicies = []

for index,row in df_tickers.iterrows():
    item = row['Name']
    if(ticker_is_primary(item)):
        ticker_indicies.append(index)
        company_name = string_normalize(item)
        df_tickers.at[index,'Name'] = company_name
df_tickers = df_tickers[df_tickers.index.isin(ticker_indicies)]

    
df_tickers.to_csv("normalized tickers.csv",index=False)