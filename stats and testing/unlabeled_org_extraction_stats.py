#!/usr/bin/env python
# coding: utf-8

# In[3]:


import re
import numpy as np
import pandas as pd
import difflib
import transformers
import spacy
from transformers import BertTokenizerFast


# In[4]:


df_labels = pd.read_csv("news_handled/new_nasdaq_labeled_companies_holdings.csv",index_col=False,header=0)
df_all_extracted_companies = pd.read_csv("news_handled/new_all_companies_nasdaq_normalized.csv",index_col=False,header=0)
df_news = pd.read_csv("news_handled/nasdaq_news.csv",index_col=False,header=0)
df_tickers = pd.read_csv("new handling normalized tickers holdings with industry.csv",index_col=False,header=0)


# In[5]:


nlp = spacy.load("en_core_web_sm")
COMMENT = ""
print(df_all_extracted_companies['Name'][0])


# In[6]:


tokenizer = transformers.BertTokenizerFast.from_pretrained("dslim/bert-base-NER")


# In[7]:


commonly_used_words = ["of","america","american","taiwan","banco","mexico","china","health","healthcare","pharma","pharmaceutical","us","partners","united states","managment","mosaic",
                       "financial","bank","companies","services","products","brands","air","airlines","international","asset","equity","fund","group","resourses","technologies","hotels","control","controls","black","green","natural","steel","motor",
                       "general","resourses","electric","payments","home","world","union","credit","business","public","shipping","capital","express","royal","mobile","microelectronics"
                       "first","exchange","block","united","energy","national","realty","york","titan","community","skin","foods","industrial","iron","paper","crown","petroleum","jewelers"]


# In[8]:


def is_valid_match(real_str, extracted_str):
    global COMMENT
    
    all_real_words_is_common = True
    all_extracted_words_is_common = True
    real_words = real_str.lower().replace("-"," ").split(" ")#for walmart and other
    extracted_words = extracted_str.lower().replace("-"," ").split(" ")
    
    
    for word in real_words:
        if(word not in commonly_used_words and len(word) > 3):
            all_real_words_is_common = False
            
    if(all_real_words_is_common):
        COMMENT = "all words in real is commonly used, only full match avaliable"
        return False
    
    
    for word in extracted_words:
        if(word not in commonly_used_words and len(word) > 3):
            all_extracted_words_is_common = False
    if(all_extracted_words_is_common):
        COMMENT = "all words in extracted company is commonly used, only full match avaliable"
        return False
    
    if(len(real_words) > 1 and len(extracted_words) > 1 and real_str.replace(" ","").find(extracted_str)!=-1 ):
        COMMENT = "Vaild words match"
        return True
    
    for word in extracted_words:
        if(word not in real_words):
            return False
    COMMENT = "Vaild words match"
    return True


# In[9]:


def is_also_proper(real_str, extracted_str,nlp):
    global COMMENT
    doc = nlp(real_str)
    
    for tok in doc: 
        if(tok.pos_ == 'PROPN' and extracted_str.replace("-","").title().find(tok.text)==-1 and tok.text not in tokenizer.get_vocab() and len(tok.text)>3 and tok.text.lower not in commonly_used_words):
            return False
        if(not tok.text.isupper() and tok.text.lower() not in commonly_used_words and tok.pos_ == 'PROPN' and extracted_str.replace("-","").title().find(tok.text)!=-1 and len(tok.text)>3):
            COMMENT = "Both companies have same proper name"
            return True
    return False


# In[10]:


def is_also_person(real_str, extracted_str,nlp):
    global COMMENT
    doc = nlp(real_str)
    for ent in doc.ents: 
        if(ent.label_ == 'PERSON' and extracted_str.find(ent.text)!=-1 and len(ent.label > 2)):
            COMMENT = "Both companies have same person name"
            return True
    return False


# In[11]:


def is_both_unique(real_str, extracted_str):#check if organisation name contains unique word
    global COMMENT
    real_words = real_str.replace("-","").split(" ")
    extracted_words = extracted_str.replace("-","").split(" ")
    if(len(real_words)==1 and len(extracted_str.replace("-","").split(" "))==1):#one subword - not valid
        return False
    for word in real_words:
        if(word in extracted_words and word not in tokenizer.get_vocab() and word.lower() not in commonly_used_words):
            COMMENT = "Both companies have unique word"
            return True
    words = real_str.split(" ")
    for word in words:
        if(word in extracted_words and word not in tokenizer.get_vocab() and word.lower() not in commonly_used_words):
            COMMENT = "Both companies have unique word"
            return True
    return False


# In[12]:


def is_extracted_contain_real(real_str, extracted_str):#check if organisation name contains person name
    if(extracted_str.find(real_str) !=-1):
        return True
    words = real_str.replace("-"," ").lower().split(" ")
    extracted_words = extracted_str.replace("-"," ").lower().split(" ")
    for word in words:
        if(word not in extracted_words):
            return False
    return True


# In[13]:


def is_abbreviation(real_str, extracted_str):
    global COMMENT
    company = real_str.lower()
    extracted = extracted_str.replace("-"," ").lower().split(" ")
    extracted = [elem for elem in extracted if len(elem)!=0]
    if not(extracted and company):
        return False
    if(len(company)!=len(extracted)): 
        if(company[-1] == 'c' or company[-1] == 'g'):
            extracted.append(company[-1])
    if(len(company)!=len(extracted)):
        return False
    
    for idx in range(len(extracted)):
        if(company[idx]!=extracted[idx][0]):
            return False
    COMMENT = "Company is abbreviation"
    return True


# In[14]:


def common_mixed_word(real_str, extracted_str):#check if organisation name contains unique word
    global COMMENT
    real_words = real_str.replace("-","").split(" ")
    extracted_words = extracted_str.replace("-","").split(" ")
    if(len(real_words)==1 and len(extracted_str.replace("-","").split(" "))==1):#one subword - not valid
        return False
    for word in real_words:
        if(word in extracted_words  and not word.isupper() and not word.islower() and not word.istitle()):
            COMMENT = "Both companies common mixed word"
            return True


# In[ ]:


def only_commonly_used_is_common(real_words, extracted_words):
    isOkay = False
    for word in real_words:
        if(word in extracted_words and word not in commonly_used_words):
            return False
        elif(word in extracted_words and word in commonly_used_words):
            isOkay = True
    return isOkay


# In[15]:


print(is_extracted_contain_real("Alcoa","Gary Hill"))


# In[18]:


#matching:
res_df = pd.DataFrame(columns=['Real company','Ticker company','Extracted company','Metrix','Comment','Article'])

found_num = 0
not_found_num = 0
total = 0

labeled_companies = df_labels['Name']
ticker_companies = df_tickers['Name']
news = df_news['News']
#ARTICLES_NUM = len(labeled_companies)
ARTICLES_NUM = 100

extracted_companies = df_all_extracted_companies['Name']
print(extracted_companies[0])
perfect_companies = 0
contain_real_companies = 0

for idx in range (ARTICLES_NUM):
    labeled = labeled_companies[idx].split('\t')
    extracted = set(extracted_companies[idx].split('\t'))#?set worked!
    total += len(labeled)
    print(idx)
    for labeled_elem in labeled:
        max_metrix = 0.0
        COMMENT = ""
        isEnd = False
        extracted_idx = 0
        for extracted_elem in extracted:
            print(extracted_elem," is ",extracted_idx," elem from ", len(extracted)," total")
            extracted_idx += 1
            if(not extracted_elem or extracted_elem == 'Not Avaliable' or extracted_elem.lower() == 'nan'):
                continue
            for curr_elem in ticker_companies:
                curr_str = curr_elem.replace(" ","").replace("-","").lower()
                extracted_str = extracted_elem.replace(" ","").replace("-","").lower()
                metrix = difflib.SequenceMatcher(None,curr_str,extracted_str).ratio()
                if (metrix < 0.3 or extracted_elem == 'Not Avaliable'):
                    continue
                if (metrix == 1.0 or curr_str.replace("group","") == extracted_str or curr_str.replace("&","and") == extracted_str or extracted_str.replace("&","and") == curr_str):
                    max_elem = curr_elem
                    
                    max_metrix = 1.0
                    best_extracted = extracted_elem
                    perfect_companies += 1
                    #isEnd = True
                    break
                if (is_extracted_contain_real(curr_elem,extracted_elem) and len(curr_elem) > 3):
                    max_elem = curr_elem
                    best_extracted = extracted_elem
                    print("OK, for sure? ",max_elem, best_extracted)
                    max_metrix = 1.0
                    contain_real_companies += 1
                    #isEnd = True
                    break
                if (metrix > 0.3 and len(extracted_str) > 2 and (len(curr_str) > 2) and (is_valid_match(curr_elem,extracted_elem) or is_valid_match(extracted_elem,curr_elem) or is_also_proper(curr_elem,extracted_elem,nlp) or is_both_unique(curr_elem,extracted_elem))):
                    if(0.86 > max_metrix):
                        max_metrix = 0.86
                        max_elem = curr_elem
                        best_extracted = extracted_elem
                if (is_abbreviation(curr_elem,extracted_elem) or is_abbreviation(extracted_elem,curr_elem)):
                    if(0.81 > max_metrix):
                        max_metrix = 0.81
                        max_elem = curr_elem
                        best_extracted = extracted_elem
                if common_mixed_word(extracted_elem,curr_elem):
                    if(0.85 > max_metrix):
                        max_metrix = 0.85
                        max_elem = curr_elem
                        best_extracted = extracted_elem
                if metrix > max_metrix:
                    max_metrix = metrix
                    max_elem = curr_elem
                    best_extracted = extracted_elem
                    COMMENT = ""
            #if (isEnd):
            #    break
            if (max_metrix > 0.90) or (max_metrix > 0.8  and len(curr_elem) > 2 and len(max_elem) > 2):      
                res_df.loc[found_num]=[labeled_elem,max_elem,best_extracted,max_metrix,COMMENT,news[idx]]
                max_mertix = 0
        if (max_metrix > 0.90) or (max_metrix > 0.8  and len(curr_elem) > 2 and len(max_elem) > 2):      
            #res_df.loc[found_num]=[labeled_elem,max_elem,best_extracted,max_metrix,COMMENT,news[idx]]
            found_num += 1
        else:
            not_found_num += 1
            print(labeled_elem,"+", extracted," best: ",max_elem," :idx = ",idx)
print("not found", not_found_num)
print("found", found_num)
print("total",total)
print("found_res = ",found_num/total)
print("perfect_res = ",perfect_companies/total)
print("contained_res = ",contain_real_companies/total)
print(res_df.count())
res_df.drop_duplicates(subset=['Real company','Extracted company'],inplace=True)
print(res_df.count())


# In[19]:


res_df.to_csv("blind_extraction_results/extracted_res_with_alice_improved.csv",index=False)