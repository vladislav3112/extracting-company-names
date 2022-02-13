import nltk
import pandas as pd
from nltk import ne_chunk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
def preprocess_orgs(sentence):
    res = []
    for sent in nltk.sent_tokenize(sentence):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                #print(chunk.label(), ' '.join(c[0] for c in chunk))
                if(chunk.label() == 'ORGANIZATION'):
                    res.append(' '.join(c[0] for c in chunk))
    return res


SUPPOSED_PEAK = 2400
df_news = pd.read_csv('nasdaq_labeled_news.csv',index_col=False)
news_list = []
for elem in df_news['News']:
    if(len(elem) < SUPPOSED_PEAK):
        news_list.append(elem)
all_companies = []

for article in news_list:
    curr_companies = ""
    sentences = article.split(". ")
    for sentence in sentences:
        curr_companies += preprocess_orgs(article) + '\t'
    all_companies.append(curr_companies[:-1])
    
res_df = pd.DataFrame(data=all_companies,columns=['Name'])
res_df.to_csv("bert_res_companies_nasdaq.csv",index=False)