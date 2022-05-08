from os import write
import csv
import re
import numpy as np
import pandas as pd
news_list = []

#tickers for labeled version
def get_tickers_companies_from_file():
    df_tickers = pd.read_csv('normalized tickers.csv',index_col=False,header=0)
    company_dict = dict(zip(df_tickers['Symbol'], df_tickers['Name']))
    return company_dict

# goal: get all labeled companies for every article with tickers
# we must be able to restore which company from which article
def get_tickers_companies_from_article(news,company_list,nasdaq_dict):
    curr_companies = ""
    isCompanyFound = False
    all_tickers = re.findall('\([A-Z]{1,5}\.[A-RT-Z]{1,2}\)',news)
    for supposed_ticker in all_tickers:
        supposed_ticker = str(supposed_ticker)[1:-1]
        if(supposed_ticker.find('www')==-1 and len(supposed_ticker) < 7):  
            supposed_ticker = supposed_ticker.partition('.')[0]
            #we must be sure that this company trades on NASDAQ
            if supposed_ticker in nasdaq_dict:
                isCompanyFound = True
                curr_companies += nasdaq_dict[supposed_ticker]+'\t'
    if(isCompanyFound):
        news_list.append(news)
        print(curr_companies[:-1])
        company_list.append(curr_companies[:-1])

nasdaq_tickers = get_tickers_companies_from_file()
company_list = []
labeled_df = pd.read_csv('labeled_news.csv',sep=',',index_col=False) 
for index,row in labeled_df.iterrows():
    article = row['News']
    get_tickers_companies_from_article(article,company_list,nasdaq_tickers)

res_df = pd.DataFrame(data=company_list,columns=['Name'])
res_df.to_csv("all_labeled_companies.csv",index=False)