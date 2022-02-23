import numpy as np
import re
import pandas as pd
import transformers
from transformers import pipeline, BertTokenizerFast, AutoModelForTokenClassification

SUPPOSED_PEAK = 2400
MAX_COMPANY_LEN = 40

df_news = pd.read_csv('labeled_news.csv',index_col=False)
news_list = []
for elem in df_news['News']:
    if(len(elem) < SUPPOSED_PEAK):
        news_list.append(elem)

stop_words = {"Inc","Co","Corp","Ltd","Company","Holdings","Group","Incorporated","SA","AG","SAB"}
conj_words = {"of","and"}
def get_alice_companies(article):
    companies = ""
    all_words = article.split()
    for idx in range(len(all_words)):
        curr_company = ""
        for stop_word in stop_words:
            if(all_words[idx].replace("."," ") == stop_word):        #company end found
                curr_company = stop_word
                curr_idx = idx
                while(True):
                    curr_idx -= 1
                    prev_word = all_words[curr_idx]
                    if not(prev_word.islower()):
                        if(curr_idx == 0):
                            companies += prev_word + " " + curr_company + "\t"
                            break
                        if(all_words[curr_idx].find(".")!=-1 or all_words[curr_idx].find(")")!=-1 or all_words[curr_idx].find(",")!=-1 or all_words[curr_idx].find("]")!=-1):
                            companies += curr_company + "\t"
                            break
                    elif (prev_word not in conj_words):
                        companies += curr_company + "\t"
                        break
                    curr_company = prev_word + " " + curr_company

    return companies
#  slice first X articles or wait too long
def get_alice_extention(str):
    res = ""
    all_words = str.split()
    if(all_words[0].isupper()):
        isCapital = True
    else:
        isCapital = False
    for word in all_words:
        if(word.islower() and word not in conj_words):
            return res[:-1]
        if(word.find(".")!=-1 or word.find(",")!=-1 or word.find(";")!=-1 or word.find("(")!=-1 or word.replace("."," ") in stop_words):
            return res[:-1]
        if(isCapital != word.isupper()):
            return res[:-1]
        res += word + " "
    return res[:-1]
#building model
import transformers
from transformers import pipeline
model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
tokenizer = transformers.BertTokenizerFast.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
nlp = pipeline('ner', model=model, tokenizer=tokenizer,grouped_entities=True)

all_companies = []

#for article in news_list:
#    companies = get_alice_companies(article)
#    all_companies.append(companies[:-1])

end_chars = {" ",".",",",";"}

for article in news_list:
    res = nlp(article)
    companies_found = ''
    is_iter_skip = False
    for elem in res:
        if(elem['entity_group'] == 'ORG'):      
            curr_start = elem['start']   
            curr_end = elem['end']         
            curr_company = elem['word']
            if(curr_end + 2 > len(article) or article[curr_end + 1] in end_chars or curr_end - curr_start < 2):  
                companies_found += curr_company + '\t'
            else:
                suspicious_string = article[curr_start:min(len(article) - curr_start - 1, MAX_COMPANY_LEN)]
                if(suspicious_string):
                    if(len(curr_company)<len(get_alice_extention(suspicious_string))):
                        print(curr_company)
                        print(get_alice_extention(suspicious_string))
                    curr_company = max(curr_company,get_alice_extention(suspicious_string),key=len)
                    companies_found += curr_company + '\t'
                    
    all_companies.append(companies_found[:-1])

res_df = pd.DataFrame(data=all_companies,columns=['Name'])
res_df.to_csv("bert_res_companies_full.csv",index=False)