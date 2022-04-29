#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import re
import pandas as pd
import sys

stop_words = ["--","Inc","Co","Corp","Ltd","Cos","Company","Holdings","Group","Incorporated","SA","NV","AG","SAB","Plc","Limited"]
conj_words = {"of","and","Of","And","by"}
capital_stop_words = ["CO","LTD","INC","CORP"]
special_chars = {";",",",".","]","}",")","*","_"}
all_stop_words = capital_stop_words + stop_words
print(all_stop_words)
# In[5]:


def get_alice_companies(article):
    companies = ""
    all_words = article.split()
    for idx in range(len(all_words)):
        curr_company = ""
        for stop_word in all_stop_words:
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
                    if(is_exit):
                        curr_company = prev_word + " " + curr_company
                    if(len(curr_company) < 4):
                        curr_company = curr_company + " " + stop_word
                if(stop_word in capital_stop_words and curr_company.isupper()):
                    print(curr_company)
                    curr_company = curr_company.title()
                    print(curr_company)
    return companies

# In[6]:


df_news = pd.read_csv('news_handled/nasdaq_news.csv',index_col=False)
news_list = df_news['News']


# In[7]:
print(get_alice_companies('Some small and midcap stocks on the move Tuesday ZANETT INC ZANE.O, $2.42, up 72 pct Shares of IT services provider doubled after the company said it had signed orders worth $29.7 million this year and expects to realise a major chunk of this revenue within the next 12 months. [IDnSGE65E0IS] RAM ENERGY RESOURCES INC RAME.O, $2.18, up 23 pct The company said it is exploring strategic alternatives, including a sale, refinancing or recapitalization. [IDnSGE65E0FK] POLYPORE INTERNATIONAL INC PPO.N, $20.56, up 5 pct ENER1 INC HEV.O, $3.28, up 8 pct Needham and Co started Polypore with "strong buy" and Ener1 with "buy" and said the battery makers would benefit from growing demand for lithium-ion batteries. [IDnSGE65E0IA] ATRICURE INC (ATRC.O), $6.70, up 28 pct The company shares rose a day after U.S. health regulators approved its device that helps prevent blood clots in the heart. [IDnSGE65D0JT] BAKERS FOOTWEAR GROUP INC BKRS.O, $1.21, down 38 pct The company, which specializes in fashion footwear, reported a wider first-quarter loss as its sandals failed to find favor with consumers and said that it did not achieve the minimum level of shareholders equity to remain listed on Nasdaq. [ID nSGE65E0QW] TRUBION PHARMACEUTICALS TRBN.O, $3.33, down 9 pct Trubion on Monday said its partner, Pfizer Inc (PFE.N), stopped development of their rheumatoid arthritis drug after it failed to meet the main goal of a mid-stage trial. [IDnSGE65D0JP] JAZZ PHARMACEUTICALS INC (JAZZ.O), $8.55, up 6 pct Barclays Capital raised its rating on Jazz to "overweight" from "equal-weight". CALLAWAY GOLF CO (ELY.N), $7.03, down 8 pct The golf gear maker shares fell a day after it forecast a dismal second-quarter as the recovery in the U.S. golfing industry has not picked up as it had hoped. [IDnSGE65D0JZ] KORNFERRY INTERNATIONAL INC (KFY.N), $15.91, up 14 pct The executive-search firm on Monday posted better-than-expected quarterly results, helped by higher fee revenue and stronger demand for permanent recruitment, and forecast first-quarter revenue above market estimates. [IDnSGE65D0JR] LA-Z-BOY INC (LZB.N), $10.40, down 16 pct The furniture maker and retailer on Monday reported a fourth-quarter profit that was in line with market expectations. [IDnSGE65D0J8] (Reporting by Shailesh Kuber in Bangalore)'))

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