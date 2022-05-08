#!/usr/bin/env python
# coding: utf-8

# In[2]:


import re
import numpy as np
import pandas as pd
import difflib
import transformers
import spacy
from transformers import BertTokenizerFast


# In[3]:


df_labels = pd.read_csv("ls_new_nasdaq_labeled_companies_holdings.csv",index_col=False,header=0)
df_all_extracted_companies = pd.read_csv("ls_new_all_companies_nasdaq_normalized1.csv",index_col=False,header=0)
df_news = pd.read_csv("nasdaq_news.csv",index_col=False,header=0)
df_tickers = pd.read_csv("ls new handling normalized tickers holdings with industry.csv",index_col=False,header=0)


# In[4]:


nlp = spacy.load("en_core_web_sm")
COMMENT = ""
print(df_all_extracted_companies['Name'][0])


# In[5]:


tokenizer = transformers.BertTokenizerFast.from_pretrained("dslim/bert-base-NER")


# In[6]:


commonly_used_words = ["of","america","american","taiwan","banco","mexico","china","health","healthcare","pharma","pharmaceutical","us","partners","united states","managment","mosaic","news",
                       "financial","bank","companies","services","products","brands","air","airlines","international","asset","equity","fund","group","resourses","technologies","hotels","control","controls","black","green","natural","steel","motor",
                       "general","resourses","electric","payments","home","world","union","credit","business","public","shipping","capital","express","royal","mobile","microelectronics",
                       "first","exchange","block","united","energy","national","realty","york","titan","community","skin","food","industrial","iron","paper","crown","petroleum","jewelers",
                       "federal","times","network","communications","industries","park","stock","securities","street","canada",
                       "inc","corp","ltd","time","yield","hill","canada","group"]


# In[7]:


def is_valid_match(real_words, extracted_words,real_str,extracted_str):
    global COMMENT
    
    all_real_words_is_common = True
    all_extracted_words_is_common = True    
    
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


# In[8]:


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


# In[9]:


def is_also_person(real_str, extracted_str,nlp):
    global COMMENT
    doc = nlp(real_str)
    res = False
    for ent in doc.ents: 
        if(ent.label_ == 'PERSON' and extracted_str.find(ent.text)!=-1 and len(ent) > 2):
            COMMENT = "Both companies have same person name"
            res = True
        if(ent.label_ == 'PERSON' and extracted_str.find(ent.text)!=-1 and len(ent) > 2):
            return False
    return res


# In[51]:


def is_both_unique(real_words, extracted_words):#check if organisation name contains unique word
    global COMMENT

    if(len(real_words)==1 and len(extracted_words)==1):#one subword - not valid
        return False
    for word in real_words:
        if(word in extracted_words and word not in tokenizer.get_vocab() and word.lower() not in commonly_used_words):
            COMMENT = "Both companies have unique word"
            return True
    #words = real_str.split(" ")
    #for word in words:
    #    if(word in extracted_words and word not in tokenizer.get_vocab() and word.lower() not in commonly_used_words):
    #        COMMENT = "Both companies have unique word"
    #        return True
    return False


# In[11]:


def is_extracted_contain_real(words, extracted_words):#check if organisation name contains person name
    for word in words:
        if(word not in extracted_words):
            return False
    return True


# In[12]:


def is_abbreviation(real_str, extracted_str):
    global COMMENT

    company = real_str.lower()
    abbreviation = extracted_str.replace("-"," ").lower().split(" ")
    abbreviation = [elem for elem in abbreviation if len(elem)!=0]
    if (len(abbreviation) < 3):
        return False
    if not(abbreviation and company):
        return False
    if(len(company)!=len(abbreviation)): 
        if(company[-1] == 'c' or company[-1] == 'g'):#group and company can be part of abberviation also
            abbreviation.append(company[-1])
    if(len(company)!=len(abbreviation)):
        return False
    
    for idx in range(len(abbreviation)):
        if(company[idx]!=abbreviation[idx][0]):
            return False
    COMMENT = "Company is abbreviation"
    return True


# In[13]:


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


# In[14]:


def only_commonly_used_is_common(real_words, extracted_words):
    isOkay = False
    for word in real_words:
        if(word in extracted_words and word.lower() not in commonly_used_words):
            return False
        elif(word in extracted_words and word.lower() in commonly_used_words):
            isOkay = True
    return isOkay


# In[15]:


print(is_extracted_contain_real("Alcoa","Gary Hill"))


# In[ ]:





# In[52]:


#matching:
import time
#res_df = pd.DataFrame(columns=['Real company','Ticker company','Extracted company','Metrix','Comment','Article'])

labeled_companies = df_labels['Name']
ticker_companies = df_tickers['Name']
news = df_news['News']
#ARTICLES_NUM = len(labeled_companies)
ARTICLES_NUM = 100

extracted_companies = df_all_extracted_companies['Name']
print(extracted_companies[0])
contain_real_companies = 0

#t1 = time.time()
def parallel_func(rank):
    not_found_companies = []
    res_df = pd.DataFrame(columns=['Real company','Ticker company','Extracted company','Metrix','Comment','Article','Extracted'])
    company_idx = 0
    total = 0
    found_num = 0
    extracted_str = ''
    start_value = rank*(ARTICLES_NUM//PROCESSES)
    end_value = start_value + ARTICLES_NUM//PROCESSES
    if(rank == PROCESSES - 1):
        end_value = ARTICLES_NUM
    print("Makes sence ",end_value)
    for idx in range(start_value,end_value):
        labeled = labeled_companies[idx].split('\t')
        extracted = set(extracted_companies[idx].split('\t'))#?set worked!
        total += len(labeled)
        print(idx)
        for labeled_elem in labeled:
            COMMENT = ""
            isFound = False
            extracted_idx = 0
            for extracted_elem in extracted:
                max_metrix = 0.0
                extracted_words = extracted_elem.replace("-"," ").split(" ")
                #print(extracted_elem," is ",extracted_idx," elem from ", len(extracted)," total")
                extracted_idx += 1
                extracted_str = extracted_elem.replace("-","").lower()
                #print(extracted_str)
                if(not extracted_elem or extracted_elem == 'Not Avaliable' or extracted_elem.lower() == 'nan'):
                    continue
                for curr_elem in ticker_companies:
                    curr_str = curr_elem.replace("-","").lower()
                    ticker_words = curr_elem.replace("-"," ").split(" ")#for walmart and other
                    metrix = difflib.SequenceMatcher(None,curr_str.replace(" ",""),extracted_str.replace(" ","")).ratio()
                    if (metrix < 0.2 or extracted_elem == 'Not Avaliable'):
                        continue
                    if (metrix == 1.0 or curr_str.replace(" ","").replace("group","") == extracted_str.replace(" ","") or extracted_str.replace(" ","").replace("group","") == curr_str.replace(" ","") or curr_str.replace("&","and") == extracted_str or extracted_str.replace("&","and") == curr_str):
                        max_elem = curr_elem
                        #print("Should be in the answer: ",max_elem,extracted_elem)
                        max_metrix = 1.0
                        best_extracted = extracted_elem
                        #isEnd = True
                        break
                    if (is_extracted_contain_real(ticker_words,extracted_words)) and len(curr_elem) > 3 and len(ticker_words)>1:
                        max_elem = curr_elem
                        best_extracted = extracted_elem
                        #print("OK, for sure? ",max_elem, best_extracted)
                        max_metrix = 1.0
                        #isEnd = True
                        break
                    if (max_metrix < 0.95 and is_extracted_contain_real(ticker_words,extracted_words) or extracted_str.replace(" ","").find(curr_str.replace(" ",""))!=-1) and len(curr_elem) > 3:
                        max_elem = curr_elem
                        best_extracted = extracted_elem
                        #print("OK, for sure? ",max_elem, best_extracted)
                        max_metrix = 0.95
                        #isEnd = True
                    if(only_commonly_used_is_common(ticker_words,extracted_words)):
                        continue
                    if (metrix > 0.3 and len(extracted_str) > 2 and (len(curr_str) > 2) and (is_valid_match(ticker_words,extracted_words,curr_str,extracted_str) or 
                                                                                             is_also_person(curr_elem,extracted_elem,nlp) or 
                                                                                             is_both_unique(ticker_words,extracted_words))):
                        if(0.86 + metrix/10.0) > max_metrix:
                            max_metrix = 0.86 + metrix/10.0
                            max_elem = curr_elem
                            best_extracted = extracted_elem
                    if (is_abbreviation(curr_elem,extracted_elem) or is_abbreviation(extracted_elem,curr_elem)):
                        if(0.81 + metrix/10.0 > max_metrix):
                            max_metrix = 0.81
                            max_elem = curr_elem
                            best_extracted = extracted_elem
                    if common_mixed_word(extracted_str,curr_str):
                        if(0.85 + metrix/10.0 > max_metrix):
                            max_metrix = 0.85 + metrix/10.0
                            max_elem = curr_elem
                            best_extracted = extracted_elem
                    if metrix > max_metrix:
                        max_metrix = metrix
                        max_elem = curr_elem
                        best_extracted = extracted_elem
                        COMMENT = ""
                #if (isEnd):
                #    break
                if (max_metrix > 0.90) or (max_metrix > 0.8  and len(best_extracted) > 2 and len(max_elem) > 2):
                    res_df.loc[company_idx] = [labeled_elem,max_elem,best_extracted,max_metrix,COMMENT,news[idx],extracted]
                    #print("Great! ",labeled_elem,"+", max_elem," best: ",best_extracted," :idx = ",idx)
                    #print("curr extracted elem: ",extracted_elem)
                    max_mertix = 0
                    company_idx += 1
                    if(labeled_elem == max_elem and not isFound):
                        found_num += 1
                        isFound = True
            if (not isFound):
                not_found_companies.append(labeled_elem+str(idx)) 
    return res_df,found_num,total,not_found_companies


# In[53]:


PROCESSES = 16
import multiprocessing
import time
t1 = time.time()
with multiprocessing.Pool(PROCESSES) as pool:
    results = pool.map(parallel_func, range(PROCESSES))
t2 = time.time()
print("Elapsed:",t2-t1)
missed_companies = []

# In[81]:


print(results[0][1])
total_num1 = 0
found_num1 = 0
frames = []
for i in range(PROCESSES):
    total_num1 += results[i][2]
    found_num1 += results[i][1]
    frames.append(results[i][0])
    missed_companies.append(pd.Series(results[i][3]))
print("accuracy: ",found_num1 / total_num1)
print("found:",found_num1)
print("total:",total_num1)
res = pd.DataFrame()
missed = pd.DataFrame()
res = pd.concat(frames)
missed = pd.concat(missed_companies)
print(res.head())


# In[82]:


res.to_csv("blind_extraction_results_parallel.csv",index=False)

missed.to_csv("parallel_missed_companies.csv",index=False)

