from os import write
import csv
import pandas as pd
import numpy as np
import difflib

bert_company_list = []
nasdaq_dict = {}    #ticker - company

feature_words = ["america","bank","health"]
def is_valid_match(real_str, extracted_str,nlp):
    words = real_str.split(" ")
    for word in words:
        for feature in feature_words:
            if (word.lower().find(feature)!=-1) and extracted_str.lower().find(feature)==-1:
                return False
        ner = nlp(word)
        if(len(ner)==0):
            continue
        label = ner[0]['entity_group']
        if(label == 'PER'):
            if(extracted_str.lower().find(word.lower())==-1):
                return False
    return True

df_bert = pd.read_csv('bert-markets-normalized.csv',index_col=False,header=0)
df_tickers = pd.read_csv('normalized tickers.csv',index_col=False,header=0)
df_labels = pd.read_csv('labeled_companies.csv',index_col=False,header=0)

#matching:
res_df = pd.DataFrame(columns=['Bert company','Real company','Metrix'])
found_num = 0
not_found_num = 0
total = 0

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
            labeled_str = elem.replace(" ","").replace("-","").lower()
            bert_str = bert_elem.replace(" ","").replace("-","").lower()
            metrix = difflib.SequenceMatcher(None,labeled_str,bert_str).ratio()
            if metrix > max_metrix:
                max_metrix = metrix
                max_elem = bert_elem
        if (max_metrix > 0.95) or (len(labeled_str) > 3 and max_metrix > 0.7 and is_valid_match(elem,max_elem,nlp) and is_valid_match(max_elem,elem,nlp) ): #or max_elem.find(labeled_str)!=-1 or labeled_str.find(max_elem)!=-1

            res_df.loc[found_num]=[elem,max_elem,max_metrix]
            found_num += 1
        else:
            not_found_num += 1
res_df.to_csv("bert res.csv",index=False)
print("not found", not_found_num)
print("found", found_num)
print("total",total)
print("found_res = ",found_num/total)