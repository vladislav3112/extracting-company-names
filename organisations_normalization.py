from os import write
import csv
import pandas as pd
import numpy as np
import re
country_names = {' USA',' U S',' Australia',' China',' Spain'}
stop_words = {' Company',' Corp',' Inc',' Ltd','.Com'}

special_chars ={'.',',','(',')',':','*','/',"'",'"', '&','?'}
# below - option
# and (str.find('Co') != -1 or str.find('Inc') != -1 or str.find('Corp') != -1 or str.find('Ltd') != -1 or str.find('Company') != -1)
def company_is_valid(str):
    if ((len(str) > 5)):
        return True
    else:
        return False

def string_normalize(str):
    
    #step 0: remove 's and spzces remove
    str = str.replace("'s",'')

    #step 1: legal ang special charachter removal:
    str = ''.join(re. sub(r'\([^)]*\)', '', str))
    #step 2: case normalization
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
    
    #step 4: special cases
    #xxx
    str = str.replace('IBM','International Business Machines')
    
    #str.replace('Instagram','Facebook')
    
    return str

df_orgs = pd.read_csv('bert_res_companies200.csv',index_col=False,header=0)
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