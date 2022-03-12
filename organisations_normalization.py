from os import write
import csv
import pandas as pd
import numpy as np
import re
country_names = {' USA',' U S',' Australia',' China',' Spain'}
bounder_words = {'And','Of','and','of','Shares',"-"," "}
last_words = {'Co'}
stop_words = {' Company',' Corp',' Inc',' Ltd','.Com', ' Incorporated',' Holdings',' Co ',' Securities',' Asset',' Plc',' Group'}#' Incorporated', ' Group',' Holdings' - risky option

special_chars ={'.',',','(',')',':','*','/',"'",'"', '&','?'}

def string_normalize(str):
    
    #step 0: remove 's and spaces removal
    str = ''.join(re.sub(' +', ' ', str))
    str = str.replace("'s",'')
    str = str.replace(' - ','-')
    #step 1: legal ang special charachter removal:
    str = ''.join(re.sub(r'\([^)]*\)', '', str))
    #step 2: case normalization
    if(str.islower()):
        str = str.title()
    
    for char in special_chars:
        str = str.replace(' '+char+' ',char)
        str = str.replace(' '+char,char)

    for word in stop_words:
        str = str.partition(word)[0]
        
    

    str = str.replace('J&J','JohnsonJohnson')
    
    for char in special_chars:
        str = str.replace(char,'')
    #step 3: country name removal
    for name in country_names:
        str = str.replace(name,'')
    str = str.replace('Corporation','Corp')
    str = str.replace('Cos','Companies')
    str = str.replace(' Of ',' ')
    str = str.replace('The ','')
    str = str.replace(' U S','US')
    #step 4: special cases
    
    str = str.replace('United States','US')
    str = str.replace('Jnj','JohnsonJohnson')
    str = str.replace('Jj','JohnsonJohnson')
    str = str.replace('Ibm','International Business Machines')
    str = str.replace('Instagram','Facebook')
    str = str.replace('Hp ','Hewlett-Packard ')
    str = str.replace('Ups','United Parcel Service')
    str = str.replace('Mts','Mobile Telesystems Pjsc')
    str = str.replace('Google','Alphabet')
    str = str.replace('Goog','Alphabet')
    str = str.replace('Asda','Walmart')
    str = str.replace('Citibank','Citigroup')
    str = str.replace('Grubhub','Just Eat Takeawaycom')
    str = re.sub(r'\b\w{1}\b', '', str)
    
    #step 5: strip and spaces normalization
    for word in last_words:   
        if(len(str) > len(word) and str.find(word)==len(str) - len(word)):
            str = str[:-len(word)]
    for word in bounder_words:   
        if(str.find(word)==0 or (len(str) > len(word) and str.find(word)==len(str) - len(word))):
            str = str[len(word)+1:]
    for word in bounder_words: 
        str = str.removesuffix(word)
    if(len(str)>4):
        str = re.sub("\d+", "", str)
    str = str.strip()
    for char in special_chars:
        str = str.strip(char)
    str = str.strip("-")
    return str

df_orgs = pd.read_csv('bert_res_companies.csv',index_col=False,header=0)
names = df_orgs['Name']

org_indicies = []
for index,row in df_orgs.iterrows():
    items = row['Name'].split('\t')
    items = [item for item in items if len(item) > 2 and ("." not in item or len(item) > 8) and "#" not in item] #if item is too short and have dot - it either ticker or not company
    #\t split and join back
    if(items):
        org_indicies.append(index)
        companies_list = ''
        for item in items:
            company_name = string_normalize(item)
            companies_list += company_name + '\t'
        companies_list = companies_list[:-1]
        df_orgs.at[index,'Name'] = companies_list
df_orgs = df_orgs[df_orgs.index.isin(org_indicies)]
df_orgs.to_csv("bert-markets-normalized.csv",index=False)