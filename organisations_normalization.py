from os import write
import csv
import pandas as pd
import numpy as np
import re
country_names = {' USA'}
stop_words = {' Company',' Corp',' Inc.',' Ltd','.Com', 'Shares', ' Incorporated',' Holdings',' Co ',' Securities',' Asset',' Plc'}#' Incorporated', ' Holdings' - risky option
last_words = {'Co', 'And','Of', 'Inc'}
first_words = ['And ','Of ','and ','Shares ','of ',"-"," "]
special_chars = ['.',',','(',')',':','*','/',"'",'"', '&','?',"=","_",'$']

def string_normalize(input_str):
    
    str = input_str
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
    #print("0:",str)
    for word in last_words:   #new!
        if(len(str) > len(word) and str.find(word)==len(str) - len(word)):
            str = str[:-len(word)]
    #print("01:",str)
    for word in first_words:   #new!
        if(str.find(word)==0):
            str = str[len(word):]
    #print("02:",str)
    str = str.replace('U. S.','US')
    str = str.replace('J&J','JohnsonJohnson')
    
    for char in special_chars:
        str = str.replace(char,'')
    
    #step 3: country name removal
    for name in country_names:
        str = str.replace(name,'')
    str = str.replace('Corporation','Corp')
    str = str.replace('Cos','Companies')
    str = str.replace('The ','')
    
    #step 4: special cases
    #all subsiaries
    str = str.replace('United States','US')
    str = str.replace('JPMorgan','JP Morgan')
    str = str.replace('Us','US')
    str = str.replace('S. Steel','US Steel')
    str = str.replace('Jnj','JohnsonJohnson')
    str = str.replace('Jj','JohnsonJohnson')
    str = str.replace('IBM','International Business Machines')
    str = str.replace('Instagram','Facebook')
    str = str.replace('HP ','Hewlett-Packard ')
    str = str.replace('UPS','United Parcel Service')
    str = str.replace('MTS','Mobile TeleSystems PJSC')
    str = str.replace('Google','Alphabet')
    str = str.replace('Goog','Alphabet')
    str = str.replace('ASDA','Walmart')
    str = str.replace('Citibank','Citigroup')
    str = str.replace('GrubHub','Just Eat Takeawaycom')
    str = re.sub(r'\b\w{1}\b', '', str)
    
    tmp = [elem for elem in str.split(' ') if len(elem) > 1]
    #print("1:",input_str)
    str = ' '.join(tmp)
    
    
    str = str.strip(" ")
    for char in special_chars:
        str = str.strip(char)
    str = str.strip("-")
    #print("2:",str)
    #print("\n")
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