from os import write
import csv
import numpy as np
import re
country_names = {' USA',' U S',' Australia',' China',' Spain'}
stop_words = {' Company',' Corp',' Inc',' Ltd','.Com'}

special_chars ={'.','-',',','(',')',':','*','/',"'", '&'}
# below - option
# and (str.find('Co') != -1 or str.find('Inc') != -1 or str.find('Corp') != -1 or str.find('Ltd') != -1 or str.find('Company') != -1)
def company_is_valid(str):
    if ((len(str) > 5)):
        return True
    else:
        return False

def string_normalize(str):
    
    #step 0: remove 's
    str = str.replace("'s",'')

    #step 1: legal ang special charachter removal:
    str = ''.join(re. sub(r'\([^)]*\)', '', str))
    #step 2: case normalization
    str = str.title()
    #spaces removal
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

companies_list = []
with open('bert-companies.txt', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        str = row[0]
        
        str = str.split(' ')
        for elem in str:
            if 'Co' == elem:
                str.remove(elem)
            if '' == elem:
                str.remove(elem)
        str = ' '.join(str)

        str = string_normalize(str)
        if(company_is_valid(str)):
            companies_list.append(str)

with open('bert-companies-normalized.txt','a',encoding='utf-8') as orgs_txt:
    for elem in companies_list:
        orgs_txt.write('\n')
        tmp = elem
        orgs_txt.write(tmp)