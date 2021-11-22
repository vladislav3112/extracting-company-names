from os import write
import csv
import numpy as np
import difflib

headline_list = []
news_company_list = []
nasdaq_dict = {}    #ticker - company
big_str = ''
with open('bert-markets-normalized.txt', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        big_str += ''.join([i for i in row[0] if not i.isdigit()])+'\n'#remove all digits
    news_company_list = big_str.split('\t')

#news_company_list = news_company_list[:1000]
standard_companies = []
with open('labeled-companies.txt', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        string = row[0].split('\t')
        standard_companies.append(string[:-1])

#matching:
result_array = []
max_elem = ''
sentences = []
stats = []
for news_company in news_company_list:
    news_company = news_company.split('\n')
    for elem in news_company:   
        if(elem):
            max_metrix = 0.0
            for st_news in standard_companies:
                metrix = difflib.SequenceMatcher(None,news_company,st_news).ratio()

                if metrix > max_metrix:
                    max_metrix = metrix
                    max_elem = st_news
            if max_metrix > 0.86:
                result_array.append(news_company + '|\t|' +nasdaq_dict[max_elem] + '|\t|' + max_elem + '|\t|' + str(max_metrix))
                stats+=1
with open('labeled-stats.txt','a', encoding='utf-8') as orgs_txt:
    orgs_txt.write('company from article\t actual company\t ticker\t metric value')
    for elem in result_array:
        orgs_txt.write('\n')
        orgs_txt.write(elem)