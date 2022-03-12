import numpy as np
import re
import pandas as pd
import transformers
from transformers import pipeline, BertTokenizerFast, AutoModelForTokenClassification

SUPPOSED_PEAK = 2400

df_news = pd.read_csv('labeled_news.csv',index_col=False)
news_list = []
for elem in df_news['News']:
    if(len(elem) < SUPPOSED_PEAK):
        news_list.append(elem)


import transformers
from transformers import pipeline
model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
tokenizer = transformers.BertTokenizerFast.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
nlp = pipeline('ner', model=model, tokenizer=tokenizer,grouped_entities=True)

all_companies = []

for article in news_list:
    res = nlp(article)
    companies_found = ''
    for elem in res:
        if(elem['entity_group'] == 'ORG'):      
            companies_found += elem['word'] + '\t'
                    
    all_companies.append(companies_found[:-1])

res_df = pd.DataFrame(data=all_companies,columns=['Name'])
res_df.to_csv("bert_res_companies_full.csv",index=False)