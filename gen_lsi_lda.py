from gensim import corpora, models, similarities, utils

dicionario = corpora.Dictionary.load('/home/luiztheodoro/Documentos/mestrado/iri/trab_final/wikileaks.dict')
corpus = corpora.MmCorpus('/home/luiztheodoro/Documentos/mestrado/iri/trab_final/wikileaks.mm')

print("Gerando lsi...")
lsi = models.LsiModel(corpus, id2word=dicionario, num_topics=20)
lsi.save('wikileaks.lsi')

print("Gerando lda...")
lda = models.LdaModel(corpus, id2word=dicionario, num_topics=20)                            
lda.save('wikileaks.lda')