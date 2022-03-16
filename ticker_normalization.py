import pandas as pd
import re
country_names = {' USA'}#,' Australia',' China',' Spain'
stop_words = [' Class', ' Series', ' Depositary',' Preffered'," Shares", ' Common', ' Ordinary Share',' Common Stock',' Warrant', ' Trust',' Warrants',' Units', ' Unit',' Co ',' Company',' Corp',' Inc',' Ltd',' Incorporated',' SA '," plc"," SAB "," NV",' Holdings',' Floating',' Repersenting',' ADR','PLC']

def ticker_is_primary(str):
    if (str.find(' due') == -1 and str.find(' Due') == -1 and len(str) < 80 and str.find(' Warrant') == -1 and str.find(' warrant') == -1 and str.find(' Right') == -1 and str.find('%') == -1):
        return True
    else:
        return False
special_chars =['.',',','(',')',':','*','/',"'","?","!"]
important_chars = special_chars.copy()
important_chars.append("-")
important_chars.append("&")

def string_normalize(input_str):
    
    str = input_str
    #step 0: remove 's
    str = str.replace("'s",'')

    #step 1: legal ang special charachter removal:
    str = ''.join(re. sub(r'\([^)]*\)', '', str))
    for char in special_chars:
        str = str.replace(char,'')
    #step 2: case normalization
    tmp = str.split()
    for word in tmp:
        if(word.islower()):
            word = word.title()
    str = ' '.join(tmp)
    #step 3: country name removal
    for name in country_names:
        str = str.replace(name,'')

    str = str.replace('Corporation','Corp')
    #step 4: remove words that do not needed for matching
    for word in stop_words:
        str = str.partition(word)[0]
    
    #step 5: exceptions and strip
    if(str.find("Co") == len(str) - len("Co")):
        str = str[:-len("Co")]
    if(len(str) > 3 and str.find(" and") == len(str) - len(" and")):
        str = str[:-len(" and")]
    str = str.replace("HP","Hewlett-Packard")
    str = str.replace('United States','US')
    str = str.replace('The ','')
    str = str.replace('  ',' ')
    str = str.strip()
    for char in important_chars:
        str = str.strip(char)
    return str

df_tickers1 = pd.read_csv('nasdaq_tickers.csv',index_col=False,header=0)
names = df_tickers1['Name']
tickers = df_tickers1['Symbol'] 
df_tickers = df_tickers1[df_tickers1.Symbol.str.find('^')==-1]
df_tickers = df_tickers[['Symbol','Name','Industry']]

df_experiment = df_tickers1[['Industry']]
print(df_experiment.head(50))


df_tickers = df_tickers[df_tickers.Symbol.str.len() < 5]
ticker_indicies = []

df_copy = df_tickers.copy()
for index,row in df_tickers.iterrows():
    item = row['Name']
    if(ticker_is_primary(item)):
        ticker_indicies.append(index)
        company_name = string_normalize(item)
        df_tickers.at[index,'Name'] = company_name
df_tickers = df_tickers[df_tickers.index.isin(ticker_indicies)]
print(df_copy.head())
df_copy = df_copy[df_copy.index.isin(ticker_indicies)]
print(df_copy.head())
df_copy = df_copy[['Name']]
df_copy['New cropped name'] = df_tickers['Name']

df_copy.to_csv("tickers normalization test.csv",index=False)
df_tickers.to_csv("new handling normalized tickers holdings with industry.csv",index=False)