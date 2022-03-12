from os import write
import spacy
import spacy.cli
import csv
import numpy as np
import difflib

headline_list = []
news = []
#model_sp = en_core_web_lg.load()
#for ent in model_sp(english_text).ents:
#  print(ent.text.strip(), ent.label_)
#  slice first 10000 articles
str = "And Dell Inc"
print(str[3:])
import nltk
from nltk import ne_chunk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

from transformers import pipeline, BertTokenizerFast, AutoModelForTokenClassification

from flair.models import SequenceTagger
tagger = SequenceTagger.load('ner')
from flair.data import Sentence
english_text = "TSMC (2330.TW), the worlds largest contract chip maker, sees global chip sales rising 7 percent annually between 2011 and 2016, Chairman and Chief Executive Morris Chang told the companys annual shareholders meeting. Strong demand from China will lift the growth outlook for the semiconductor market to 6 or 7 percent for the next five years, Chang had told the Financial Times in an interview published on Monday. [IDnLDE65D00A] Chang had forecast annual growth to slow to 4.2 percent in 2011-2014, partly as other new key component such as touch-screen panels are used in electronics products. [IDnTOE63D02F] Taiwan Semiconductor Manufacturing Co Ltd (TSMC) (TSM.N) posted record sales for a second month in May, buoyed by strong demand for computers and electronic gadgets. [IDnTOE65301O] TSMC has allocated record capital spending to boost capacity and upgrade technology to meet rising demand for new PCs and other consumer products that require more powerful chips. (US$1=T$32.4) (Reporting by Baker Li, Editing by Jonathan Standing)"
s = Sentence(english_text)
tagger.predict(s)
for entity in s.get_spans('ner'):
    if(entity.labels[0].value == 'ORG'):
        print(entity.text)

s1 = "Ford Motor"
s2 = "Ford"
s1 = s1.replace(" ","")
s2 = s2.replace(" ","")
print(s1)
print(s2)
print(difflib.SequenceMatcher(None,s1.lower(),s2.lower()).ratio())


from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

nlp = pipeline("ner",grouped_entities=True, model=model, tokenizer=tokenizer)
example = "JPMorgan Chase  Co (JPM.N), Bank of America Corp (BAC.N), Citigroup Inc (C.N), American Express Co (AXP.N) and Discover Financial Services (DFS.N) are expected to report the monthly performance of their credit card portfolios later. Capital One is the third-largest U.S. issuer of Visa (V.N)-branded credit card and the fifth-largest issuer of MasterCard (MA.N)-branded credit cards. Capital One shares closed at $40.46 Monday on the New York Stock Exchange."
print(example)
print("\n")

ner_results = nlp(example)
print(ner_results)

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

st = StanfordNERTagger('/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
					   '/usr/share/stanford-ner/stanford-ner.jar',
					   encoding='utf-8')

text = 'While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'

tokenized_text = word_tokenize(text)
classified_text = st.tag(tokenized_text)

print(classified_text)
