import pandas as pd
import numpy as np
import re
country_names = {' USA'}
stop_words = {' Company',' Corp',' Inc.',' Ltd','.Com', 'Shares', ' Incorporated',' Holdings',' Co ',' Securities',' Asset',' Plc'}#' Incorporated', ' Holdings' - risky option
last_words = {'Co', 'And','Of', 'Inc'}
first_words = ['And ','Of ','and ','Shares ','of ',"-"," "]
special_chars = ['!','.',',','(',')',':','*','/',"'",'"','?',"=","_",'$']
important_chars = special_chars.copy()  #new chars in list should not be removed 
important_chars.append("-")
important_chars.append("&")

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
    
    old_tmp = str.split()
    tmp = []
    for word in old_tmp:
        if(word.islower()):
            word = word.title()
        tmp.append(word)
    str = ' '.join(tmp)

    for word in stop_words:
        str = str.partition(word)[0]

    for word in last_words:  
        if(len(str) > len(word) and str.find(word)==len(str) - len(word)):
            str = str[:-len(word)]

    for word in first_words:   
        if(str.find(word)==0):
            str = str[len(word):]

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
    str = str.replace('Air Products&Chemicals','Air Products and Chemicals')
    str = str.replace('J&J','Johnson & Johnson')
    str = str.replace('IBM','International Business Machines')
    str = str.replace('Instagram','Facebook')
    str = str.replace('UPS','United Parcel Service')
    str = str.replace('MTS','Mobile TeleSystems PJSC')
    str = str.replace('Google','Alphabet')
    str = str.replace('BNY Mellon','Bank of New York Mellon')
    str = str.replace('ASDA','Walmart')
    str = str.replace('Asda','Walmart')
    str = str.replace('Citibank','Citigroup')
    str = str.replace('GrubHub','Just Eat Takeawaycom')
    
    tmp = [elem for elem in str.split(' ') if len(elem) > 1 or elem =="&"]

    str = ' '.join(tmp)
    
    str = str.strip(" ")
    for char in important_chars:
        str = str.strip(char)

    if(str == "HP"):
       str = 'Hewlett-Packard'
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