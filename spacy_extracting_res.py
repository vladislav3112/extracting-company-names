import pandas as pd
import spacy
import spacy.cli
import numpy as np

SUPPOSED_PEAK = 2400
df_news = pd.read_csv('labeled_news.csv',index_col=False)
news_list = []
for elem in df_news['News']:
    if(len(elem) < SUPPOSED_PEAK):
        news_list.append(elem)

#  slice first X articles or wait too long

#building model
all_companies = []

model_sp = spacy.load('en_core_web_lg')
for list in news_list:
    companies_found = ''
    for ent in model_sp(list).ents:
        if (ent.label_=='ORG'):
            companies_found += ent.text.strip() + '\t'
    all_companies.append(companies_found[:-1])

res_df = pd.DataFrame(data=all_companies,columns=['Name'])
res_df.to_csv("spacy_res_companies_full.csv",index=False)