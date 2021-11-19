from os import write
import csv
import numpy as np
import difflib

headline_list = []
news_company_list = []
nasdaq_dict = {}    #ticker - company

with open('bert-companies-normalized.txt', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        news_company_list.append(row[0])
#news_company_list = news_company_list[:1000]
with open('normalized tickers.txt', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        string = row[0].split(' ')
        ticker = string[0]
        del(string[0])
        string = ' '.join(string)
        nasdaq_dict[ticker] = string

#matching:
result_array = []
max_elem = ''
sentences = []
for news_company in news_company_list:
    max_metrix = 0.0
    for ticker in nasdaq_dict:
        metrix = difflib.SequenceMatcher(None,news_company,nasdaq_dict[ticker]).ratio()

        if metrix > max_metrix:
            max_metrix = metrix
            max_elem = ticker
    if max_metrix > 0.86:
        result_array.append(news_company + '|\t|' +nasdaq_dict[max_elem] + '|\t|' + max_elem + '|\t|' + str(max_metrix))

with open('matching-results-bert.txt','a', encoding='utf-8') as orgs_txt:
    orgs_txt.write('company from article\t actual company\t ticker\t metric value')
    for elem in result_array:
        orgs_txt.write('\n')
        orgs_txt.write(elem)