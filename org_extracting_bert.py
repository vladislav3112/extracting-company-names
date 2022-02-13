from os import write
import numpy as np
import pandas as pd
from sqlalchemy import between
import transformers
from transformers import pipeline, BertTokenizerFast, AutoModelForTokenClassification

SUPPOSED_PEAK = 2400
df_news = pd.read_csv('labeled_news.csv',index_col=False)
news_list = []
for elem in df_news['News']:
    if(len(elem) < SUPPOSED_PEAK):
        news_list.append(elem)

#  slice first X articles or wait too long

#building model
import transformers
from transformers import pipeline
model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
tokenizer = transformers.BertTokenizerFast.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
nlp = pipeline('ner', model=model, tokenizer=tokenizer,grouped_entities=True)

all_companies = []

for article in news_list:
    res = nlp(article)
    companies_found = ''
    is_iter_skip = False
    for elem_idx in range(len(res)-1):
        if(is_iter_skip):
            is_iter_skip = False
            continue
        if(res[elem_idx]['entity_group'] == 'ORG'):      
            prev_end = res[elem_idx]['end']         
            prev_company = res[elem_idx]['word']    
            if(res[elem_idx + 1]['entity_group'] == 'ORG'):
                curr_company = res[elem_idx + 1]['word']     #goal - if there is less then 1 space between companies
                curr_start = res[elem_idx + 1]['start']      #- that is the same company
                between_companies_str = article[prev_end:curr_start]
                if(between_companies_str.count(" ") < 2 and between_companies_str.find("(") == -1  and between_companies_str.find(")") == -1 and between_companies_str.find(".") == -1 and between_companies_str.find(".") == -1):
                    companies_found += res[elem_idx]['word'] + " " + res[elem_idx + 1]['word'] + '\t'
                    is_iter_skip = True
                else:
                    companies_found += res[elem_idx]['word'] + '\t'
            else:
                companies_found += res[elem_idx]['word'] + '\t'
    all_companies.append(companies_found[:-1])

res_df = pd.DataFrame(data=all_companies,columns=['Name'])
res_df.to_csv("bert_res_companies_full.csv",index=False)