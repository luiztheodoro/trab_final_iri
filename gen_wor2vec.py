import pandas as pd
from gensim import models, similarities, utils
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

sentences = list(MySentences())

print("Gerando modelo w2v...")
model_w2v = models.Word2Vec(sentences, min_count=5)
model_w2v.save('/home/luiztheodoro/Documentos/mestrado/iri/trab_final/wikileaks.w2v')