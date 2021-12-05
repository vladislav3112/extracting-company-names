from os import write
import csv
import re
import difflib
import numpy as np
import pandas as pd
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

news_list = []

df_companies = pd.read_csv('labeled_news.csv',index_col=False)
news_list = df_companies['News']

#  slice first X articles or wait too long

#building model
import transformers
from transformers import pipeline
model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
tokenizer = transformers.BertTokenizerFast.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
nlp = pipeline('ner', model=model, tokenizer=tokenizer,grouped_entities=True)


curr_idx = 0
all_companies = []
news_list = news_list[:200]

for article in news_list:
    res = nlp(article)
    companies_found = ''
    for elem in res:
        if(elem['entity_group'] == 'ORG'):      
            companies_found += elem['word'] + '\t'
    all_companies.append(companies_found[:-1])

res_df = pd.DataFrame(data=all_companies,columns=['Name'])
res_df.to_csv("bert_res_companies200.csv",index=False)