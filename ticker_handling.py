from os import write
import csv
import numpy as np

with open('organisations list.txt', 'r', encoding='utf-8') as file:
    companies_text = file.read()

headline_list = []
news_list = []
nasdaq_dict = {}    #ticker - company
with open('nasdaq_tickers.csv', 'r',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
            nasdaq_dict[row[0]] = row[1]
with open('company-tickers.txt','a',encoding='utf-8') as orgs_txt:
    for elem in nasdaq_dict:
        #orgs_txt.write('\n')
        tmp = elem+' '+nasdaq_dict[elem]
        #orgs_txt.write(tmp)

# text similarity ways
# 1. tf-idx 
# 2. levenstain - worsest
# 3. networts (bart maybe)
# 4. 

# 1:
import difflib
from Levenshtein import distance
a = 'Apple Inc.'# 0.6 res
b = 'Apple Inc. Common Stock'
seq = difflib.SequenceMatcher(a=a.lower(), b=b.lower())
print(seq.ratio())

a = 'Apple Inc.'# 0.84 res
b = 'Apple Co.'
seq = difflib.SequenceMatcher(a=a.lower(), b=b.lower())
print(seq.ratio())

a = 'Apple'#0.66 res
b = 'Appleby 46'
seq = difflib.SequenceMatcher(a=a.lower(), b=b.lower())
print(seq.ratio(), " Appleby")

a = 'The New York Times Co'#0.79 res  !!!THE!!!
b = 'New York Times Company'
seq = difflib.SequenceMatcher(a=a.lower(), b=b.lower())
print(seq.ratio())
#interesting, worth to check( apple and pineapple <0.65 score)

#2
print(distance("Apple Inc.","Apple Co."))
print(distance("Apple","Appleby"))
print(distance("The New York Times Co","New York Times Company"))
#if compute loss as dist/minlen -> 3rd is worsest!!!

#3 bert usage

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

print(cosine_similarity(
    [sentence_embeddings[0]],
    sentence_embeddings[1:]
))

#result:    1-3 best pairs
#           4-5 0.976 score
#           0.31 for (apple - pineapple)