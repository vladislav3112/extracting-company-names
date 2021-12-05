from os import write
import csv
import pandas as pd
import numpy as np
import difflib

bert_company_list = []
nasdaq_dict = {}    #ticker - company

df_bert = pd.read_csv('bert-markets-normalized.csv',index_col=False,header=0)
df_tickers = pd.read_csv('normalized tickers.csv',index_col=False,header=0)
df_labels = pd.read_csv('labeled_companies.csv',index_col=False,header=0)

#matching:
res_df = pd.DataFrame(columns=['Bert company','Real company','Metrix'])
real_companies_num =  0
bert_companies_num =  0
found_num = 0
not_found_num = 0
matches = 0

ARTICLES_NUM = 200

labeled_companies = df_labels['Name']
labeled_companies = labeled_companies[:ARTICLES_NUM]
bert_companies = df_bert['Name']

for idx in range (ARTICLES_NUM):
    labeled = labeled_companies[idx].split('\t')
    bert = bert_companies[idx].split('\t')
    max_metrix = 0.0
    for elem in labeled:
        for bert_elem in bert:
            metrix = difflib.SequenceMatcher(None,elem.lower(),bert_elem.lower()).ratio()
            if metrix > max_metrix:
                max_metrix = metrix
                max_elem = bert_elem
        if max_metrix > 0.69:
            res_df.loc[found_num]=[elem,max_elem,max_metrix]
            found_num += 1
            max_metrix = 0.0
        else:
            not_found_num += 1
res_df.to_csv("bert res.csv",index=False)
print("not found", not_found_num)
print("found", found_num)