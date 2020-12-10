import string
import numpy as np
import datetime
import spacy
import gensim

from cablemap.core import cables_from_source
from gensim import corpora, models, similarities, utils
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import stem_text, strip_punctuation, \
    strip_short, strip_multiple_whitespaces, \
    strip_non_alphanum, strip_tags, STOPWORDS
from gensim.models import CoherenceModel
from nltk.corpus import stopwords

fname = "/home/luiztheodoro/Documentos/mestrado/iri/trab_final/wikileaks-cables/cables.csv"

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

# def make_trigrams(texts):
#     return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

def telegrams():
    fname = "/home/luiztheodoro/Documentos/mestrado/iri/trab_final/wikileaks-cables/cables.csv"
    for j, cable in enumerate(cables_from_source(fname)):
        if j == 100000:
            break
        print("Gerando telegrama {}".format(j),end='\r')
        content = getattr(cable, 'content')
        content = content[content.find("1. "):len(content)-1].lower()
        content = strip_punctuation(content)
        content = strip_non_alphanum(content)
        yield simple_preprocess(content, min_len=3, deacc=True)
        
stop_words = stopwords.words('english')
stop_words.extend(['unclassified', 'confidential', 'amembassy', 'page', \
                    'official', 'percent'])

telegrams_words = list(telegrams())

# print("Criando base de bigramas...")
# bigram = gensim.models.Phrases(telegrams_words, min_count=5, threshold=100) # higher threshold fewer phrases.
# trigram = gensim.models.Phrases(bigram[telegrams_words], threshold=100)  
# bigram_mod = gensim.models.phrases.Phraser(bigram)
# trigram_mod = gensim.models.phrases.Phraser(trigram)

print("Removendo stopwords...")
telegrams_words_nostops = remove_stopwords(telegrams_words)

# print("Criando bigramas...")
# telegrams_words_bigrams = make_bigrams(telegrams_words_nostops)

# Return a Language object with the loaded model
print("Gerando modelo do Spacy...")
nlp = spacy.load('en', disable=['parser', 'ner'])

print("Lematizando os telegramas...")
#['NOUN', 'ADJ', 'VERB', 'ADV']
telegrams_lemmatized = lemmatization(telegrams_words_nostops, allowed_postags=['NOUN', 'VERBS'])

print("Criando dicionário...")
dicionario = corpora.Dictionary(telegrams_lemmatized)
dicionario.save('wikileaks.dict')

print("Criando corpus...")
corpus = [dicionario.doc2bow(d) for d in telegrams_lemmatized]
corpora.MmCorpus.serialize('wikileaks.mm', corpus)