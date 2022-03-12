english_text = "Mongolia plans to list its Oyu Tolgoi mine, one of the world biggest untapped copper and gold deposits, and is receiving proposals from global stock exchanges to assist with turning its state-run stock market into a private enterprise, a government official said on Tuesday. Mongolia hoped to list Oyu Tolgoi on the domestic exchange and an international one, Sugar Dulam, chairman of the State Property Committee of Mongolia, said at the Mongolia Capital Raising Conference. Mongolia is attracting attention from global investors after it sealed a deal in October with Ivanhoe Mines (IVN.TO) and Rio Tinto (RIO.AX) (RIO.L) to develop the Oyu Tolgoi mine, which some estimate could be worth around $3 billion. Dulam also said that Mongolia planned to list Tavan Tolgoi, one of the world largest untapped coal deposits. He added that the London Stock Exchange, the Nasdaq and the Hong Kong Stock Exchange were among the groups that had submitted proposals to Mongolia to assist in privatising its exchange."


def stanza_nlp(text):
  nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')
  doc = nlp(text)
  print(*[f'entity: {ent.text}' for sent in doc.sentences for ent in sent.ents if ent.type == 'ORG'], sep='\n')


import pandas as pd
import spacy
import stanza
import spacy.cli
import numpy as np
stanza.download('en')

SUPPOSED_PEAK = 2400
df_news = pd.read_csv('labeled_news.csv',index_col=False)
news_list = df_news['News'] 

#  slice first X articles or wait too long

#building model
all_companies = []

nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')
for article in news_list:
    companies_found = ''
    doc = nlp(article)
    for ent in article.ents:
        if (ent.label_=='ORG'):
            companies_found += ent.text.strip() + '\t'
    all_companies.append(companies_found[:-1])

res_df = pd.DataFrame(data=all_companies,columns=['Name'])
res_df.to_csv("spacy_res_companies_full.csv",index=False)