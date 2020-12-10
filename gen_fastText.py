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

print("Gerando FastText...")
model_ft = models.FastText(size=100)
model_ft.build_vocab(sentences)
model_ft.train(sentences = sentences, \
                epochs = model_ft.epochs, \
                total_examples = model_ft.corpus_count, \
                total_words = model_ft.corpus_total_words)

model_ft.save('/home/luiztheodoro/Documentos/mestrado/iri/trab_final/wikileaks.ft')