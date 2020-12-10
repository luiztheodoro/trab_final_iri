import pandas as pd
from gensim import models, similarities, utils, corpora
from gensim.utils import tokenize
from sqlalchemy import create_engine

sentences = []
con = create_engine('sqlite://///home/luiztheodoro/Documentos/mestrado/iri/trab_final/wikileaks.sqlite', echo = False)
df = pd.read_sql('wikileaks',con,)

class MySentences(object):
    
    def __init__(self):
        self.con = create_engine('sqlite://///home/luiztheodoro/Documentos/mestrado/iri/trab_final/wikileaks.sqlite', \
                    echo = False)
        self.df = pd.read_sql('wikileaks',con,)
 
    def __iter__(self):
        for index, row in self.df.iterrows():
            yield row['lista'].split(" ")

sentences = MySentences()

print("Criando dicionário...")
dicionario = corpora.Dictionary(sentences)
dicionario.save('wikileaks.dict')

print("Criando corpus...")
corpus = [dicionario.doc2bow(d) for d in sentences]
corpora.MmCorpus.serialize('wikileaks.mm', corpus)