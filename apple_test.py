from os import write
import spacy
import spacy.cli
import csv
import numpy as np

headline_list = []
news = []
#model_sp = en_core_web_lg.load()
#for ent in model_sp(english_text).ents:
#  print(ent.text.strip(), ent.label_)
#  slice first 10000 articles
companies_found = set()
str = ''
with open('apple.txt', 'r',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if(len(row) > 0):
            str += ''.join(row)
news.append(str)

model_sp = spacy.load('en_core_web_lg')
for list in news:
    for ent in model_sp(list).ents:
        if (ent.label_=='ORG'):
            companies_found.add(ent.text.strip())

with open('tmp.txt','a',encoding='utf-8') as orgs_txt:
    for company in companies_found:
        orgs_txt.write('\n')
        orgs_txt.write(company)