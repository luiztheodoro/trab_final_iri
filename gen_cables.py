import string
import numpy as np
import pandas as pd
import datetime
import spacy
import gensim

from cablemap.core import cables_from_source
from gensim import corpora, models, similarities, utils
from gensim.utils import tokenize, simple_preprocess
from gensim.parsing.preprocessing import stem_text, strip_punctuation, \
    strip_short, strip_multiple_whitespaces, strip_short, \
    strip_non_alphanum, strip_tags, STOPWORDS
from gensim.models import CoherenceModel
from nltk.corpus import stopwords

from sqlalchemy import create_engine


fname = "/home/luiztheodoro/Documentos/mestrado/iri/trab_final/wikileaks-cables/cables.csv"

stop_words = stopwords.words('english')
stop_words.extend(['unclassified', 'confidential', 'amembassy', 'page'])

def remove_stopwords(s):
    s = utils.to_unicode(s)
    return " ".join(w for w in s.split() if w not in stop_words)   

def lemmatization(s, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    doc = nlp(s) 
    return " ".join([token.lemma_ for token in doc if token.pos_ in allowed_postags])

def telegrams():
    df = pd.DataFrame(columns=['index','lista'], )
    for j, cable in enumerate(cables_from_source(fname)):
        print("Gerando telegrama {}".format(j),end='\r')
        content = getattr(cable, 'content')
        content = content[content.find("1. "):len(content)-1].lower()
        content = strip_short(content, minsize=3)
        content = strip_punctuation(content)
        content = strip_non_alphanum(content)
        content = remove_stopwords(content)
        content = lemmatization(content,['NOUN'])
        df = df.append({'lista':content, 'index': j}, ignore_index=True,)
    return df  

print("Criando telegramas...")
nlp = spacy.load('en', disable=['parser', 'ner'])
df = telegrams()
engine = create_engine('sqlite://///home/luiztheodoro/Documentos/mestrado/iri/trab_final/wikileaks.sqlite', echo = False)
df.to_sql('wikileaks',engine)