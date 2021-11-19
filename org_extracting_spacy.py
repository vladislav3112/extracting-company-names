from os import write
import spacy
import spacy.cli
import csv
import numpy as np

headline_list = []
news_list = []

with open('100k_news.csv', 'r',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        handled_row = ''.join(row).split('\t')
        if(len(handled_row) > 5):    
            headline_list.append(handled_row[4])
            article = handled_row[6].replace("\'s","s")
            news_list.append(article)
        else:
            print(handled_row)

#  slice first 10000 articles
news_list = news_list[:10000]
companies_found = set()

model_sp = spacy.load('en_core_web_lg')
for list in news_list:
    for ent in model_sp(list).ents:
        if (ent.label_=='ORG'):
            companies_found.add(ent.text.strip())

with open('finance companies.txt','a',encoding='utf-8') as orgs_txt:
    for company in companies_found:
        ss = ')'
        #orgs_txt.write('\n')
        #orgs_txt.write(company)