from os import write
import csv
import re
import difflib
import numpy as np
import pandas as pd
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

news_list = []

#tickers for labeled version
def get_tickers_companies_from_file():
    df_tickers = pd.read_csv('normalized tickers.csv',index_col=False,header=0)
    company_dict = dict(zip(df_tickers['Symbol'], df_tickers['Name']))
    return company_dict

# goal: get all labeled companies for every article with tickers
# we must be able to restore which company from which article
def get_tickers_companies_from_article(news,company_list,nasdaq_dict):
    isCompanyFound = False
    curr_list = []
    while(news.find(")")-news.find("(")>2 and news.find("(")!=-1):
        supposed_ticker = news[news.find("("):news.find(")")+1]
        #delete ticker to be ready for searching next company ticker
        news = news.replace(supposed_ticker,'')
        supposed_ticker = supposed_ticker[1:-1]
        if(len(supposed_ticker) > 0 and supposed_ticker.find('.')!=-1 and re.match("^[A-Za-z.]*$", supposed_ticker)
            and supposed_ticker.find('www')==-1 and len(supposed_ticker) < 7):  #we want skip websites but not tickers
                supposed_ticker = supposed_ticker.partition('.')[0]
                #we must be sure that this company trades on NASDAQ
                if supposed_ticker in nasdaq_dict:
                    curr_list.append(nasdaq_dict[supposed_ticker]+'\t')
                    isCompanyFound = True
    if(isCompanyFound):
        company_list.append(curr_list)
        news_list.append(news) 

nasdaq_tickers = {}
company_list = []
nasdaq_tickers = get_tickers_companies_from_file()

df_news_header = ['uuid default','date_created','date_modified','date_published','headline','description','article','article_section','author_type','author_names','reuters_keywords','Append_1','Append_2','Append_3','Append_4','Append_5','url1','url2']
df_news = pd.read_csv('100k_news.csv',sep='\t',index_col=False,names=df_news_header) 
labeled_df = df_news.loc[df_news['article_section']=='Markets'] # to filter only labeled data otherwise len(handled_row) > 5
labeled_df['article'] = labeled_df['article'].replace({"\'s","s"},regex=True)
for index,row in labeled_df.iterrows():
    article = row['article']
    get_tickers_companies_from_article(article,company_list,nasdaq_tickers)
                

       

#  slice first X articles or wait too long
#news_list = news_list[:1000]
companies_found = []
res_df = pd.DataFrame(data=news_list,columns=['News'])
res_df.to_csv("labeled_news.csv",index=False)

#building model
from transformers import pipeline
model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
nlp = pipeline('ner', model=model, tokenizer=tokenizer)

curr_company = ''
curr_idx = 0
article_idx = 0 #for labeled data only
for article in news_list:
    res = nlp(article)
  
    for elem in res:
        if(elem['entity'] == 'I-ORG'):      
            if(curr_idx != 0 and elem['index']-curr_idx > 1):
                companies_found.append(curr_company)
                curr_company = ''
            
            curr_idx = elem['index']
            
            if(elem['word'].find('#') != -1):       #you need to concat 
                curr_company += elem['word'].replace('#','')
            else:
                curr_company = curr_company + ' ' + elem['word']    #when company contains more than 1 word
        elif(elem['entity'] == 'B-ORG'):
            companies_found.append(curr_company)
            curr_company = elem['word']
        elif(curr_company):
            companies_found.append(curr_company)
            curr_company = ''
    
    article_idx += 1
    companies_found.append('\t'+str(article_idx))


with open('bert-markets.txt','a',encoding='utf-8') as orgs_txt:
    for company in companies_found:
        orgs_txt.write('\n')
        orgs_txt.write(company)