#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import re
import pandas as pd
import sys

stop_words = {"--","Inc","Co","Corp","Ltd","Cos","Company","Holdings","Group","Incorporated","SA","NV","AG","SAB","Plc","Limited"}
conj_words = {"of","and"}
special_chars = {";",",",".","]","}",")","*","_"}


# In[5]:


def get_alice_companies(article):
    companies = ""
    all_words = article.split()
    for idx in range(len(all_words)):
        curr_company = ""
        for stop_word in stop_words:
            if(all_words[idx].replace(".","") == stop_word):        #company end found
                curr_company = stop_word + "\t"
                curr_idx = idx
                is_exit = True
                while(is_exit):
                    curr_idx -= 1
                    prev_word = all_words[curr_idx]
                    if not(prev_word.islower()):
                        if(curr_idx == 0):
                            companies += prev_word + " " + curr_company
                            is_exit = False
                        for special_char in special_chars:
                            if(all_words[curr_idx].find(special_char)!=-1):
                                companies += curr_company
                                is_exit = False
                    elif (prev_word not in conj_words):
                        companies += curr_company
                        is_exit = False
                    curr_company = prev_word + " " + curr_company
                    if(len(curr_company) < 4):
                        curr_company = curr_company + " " + stop_word
    return companies


# In[6]:


df_news = pd.read_csv('news_handled/nasdaq_news.csv',index_col=False)
news_list = df_news['News']


# In[7]:


all_companies = []
idx = 0
for article in news_list:
    if(idx % 5000 ==0):
        print(idx)
    companies = get_alice_companies(article)
    all_companies.append(companies[:-1])
    idx += 1


# In[9]:


res_df = pd.DataFrame(data=all_companies,columns=['Name'])
res_df.to_csv("news_handled/ls_alice_companies_full.csv",index=False)


# concat liza and bert results:


df_1 = pd.read_csv('news_handled/ls_alice_companies_normalized.csv',index_col=False,header=0)
df_2 = pd.read_csv('news_handled/ls_bert_companies_normalized.csv',index_col=False,header=0)
result = pd.DataFrame()
result["Name"] = df_1["Name"] + "\t" + df_2["Name"]
result["Name"] = result["Name"].fillna("Not Avaliable")


# In[11]:


result.to_csv("news_handled/ls_new_all_companies_nasdaq_normalized.csv",index=False)