from os import write
import csv
import numpy as np
import difflib
from Levenshtein import distance
import pandas as pd

headline_list = []
news_list = []
nasdaq_dict = {}    #ticker - company
nasdaq_df = pd.read_csv('nasdaq_tickers.csv',header=0)
nasdaq_df = nasdaq_df[['Symbol','Name']]
nasdaq_df.to_csv("company-tickers.csv",index=False)

# text similarity ways
# 1. tf-idx 
# 2. levenstain - worsest
# 3. networts (bert maybe)
# 4. 

# 1:

a = 'Bank of China'# 0.67 res ! different companies
b = 'Bank of America'
seq = difflib.SequenceMatcher(a=a.lower(), b=b.lower())
print("bank")
print(seq.ratio())

a = 'Apple Inc.'# 0.84 res
b = 'Apple Co.'
seq = difflib.SequenceMatcher(a=a.lower(), b=b.lower())
print(seq.ratio())

a = 'Ford Motors'#0.76 res
b = 'Boston'
seq = difflib.SequenceMatcher(a=a.lower(), b=b.lower())
print(seq.ratio(), " Ford")

a = 'Bank Of America Merrill Lynch'#0.79 res  !!!THE!!!
b = 'Bank Of America'
seq = difflib.SequenceMatcher(a=a.lower(), b=b.lower())
print(seq.ratio()," America")
#interesting, worth to check( apple and pineapple <0.65 score)

#2
print(distance("Apple Inc.","Apple Co."))
print(distance("Apple","Appleby"))
print(distance("The New York Times Co","New York Times Company"))
#if compute loss as dist/minlen -> 3rd is worsest!!!

#3 bert usage
a = 'Honda Motors'#0.79 res  !!!THE!!!
b = 'Hyundai Motors'
seq = difflib.SequenceMatcher(a=a.lower(), b=b.lower())
print(seq.ratio(),"OK ")
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('bert-base-nli-mean-tokens')

sentences = [
    "Apple Co.",
    "Apple Inc.",
    "Appleby",
    "New York Times Company",   
    "The New York Times Co"
    "Pineapple"
]

from sklearn.metrics.pairwise import cosine_similarity

sentence_embeddings = model.encode(sentences)



#result:    1-3 best pairs
#           4-5 0.976 score
#           0.31 for (apple - pineapple)