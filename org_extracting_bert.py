from os import write
import csv
import re
import difflib
import numpy as np
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

news_list = []
#def labeling_bert_stats(list, standard_list):
#    for news_company in list:
#        max_metrix = 0.0
#        results = []
#        for company in standard_list:
#            metrix = difflib.SequenceMatcher(None,news_company,company).ratio()
#            if metrix > max_metrix:
#                max_metrix = metrix
#                max_elem = company
#            if max_metrix > 0.90:
#                results.append(news_company + '|\t|' +company + '|\t|' + max_elem + '|\t|' + str(max_metrix))
#    return results

#tickers for labeled version
def get_tickers_companies_from_file(company_dict):
    with open('normalized tickers.txt', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            string = row[0].split(' ')
            ticker = string[0]
            del(string[0])
            string = ' '.join(string)
            company_dict[ticker] = string

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
                #print(supposed_ticker)
                #print(supposed_ticker.partition('.')[0])
    if(isCompanyFound):
        company_list.append(curr_list)
        news_list.append(article)   #somehow it worked

nasdaq_tickers = {}
company_list = []
get_tickers_companies_from_file(nasdaq_tickers)

with open('100k_news.csv', 'r',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        
        handled_row = ''.join(row).split('\t')
        if(len(handled_row) > 7 and handled_row[7]=='Markets'):    # to filter only labeled data otherwise len(handled_row) > 5
            article = handled_row[6].replace("\'s","s")
            get_tickers_companies_from_article(article,company_list,nasdaq_tickers)
                

       

#  slice first X articles or wait too long
#news_list = news_list[:1000]
companies_found = []


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
    #stats = labeling_bert_stats(companies_found,company_list[article_idx])
    #print(stats)

with open('bert-markets.txt','a',encoding='utf-8') as orgs_txt:
    for company in companies_found:
        orgs_txt.write('\n')
        orgs_txt.write(company)

with open('labeled-companies.txt','a',encoding='utf-8') as orgs_txt:
    for company in company_list:
        orgs_txt.write('\n')
        orgs_txt.write(''.join(company))