import pandas as pd
import spacy
import spacy.cli
import numpy as np
from flair.models import SequenceTagger
from flair.data import Sentence


SUPPOSED_PEAK = 2400
df_news = pd.read_csv('nasdaq_labeled_news.csv',index_col=False)
news_list = []
for elem in df_news['News']:
    if(len(elem) < SUPPOSED_PEAK):
        news_list.append(elem)

#  slice first X articles or wait too long

#building model
all_companies = []

tagger = SequenceTagger.load('ner')

for article in news_list:
    companies_found = ''
    s = Sentence(article)
    tagger.predict(s)
    for entity in s.get_spans('ner'):
        if(entity.labels[0].value == 'ORG'):
            companies_found += entity.text + '\t'
    all_companies.append(companies_found[:-1])


res_df = pd.DataFrame(data=all_companies,columns=['Name'])
res_df.to_csv("flair_res_companies_full.csv",index=False)