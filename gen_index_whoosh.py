import cablemap
import whoosh
import datetime
import os
from cablemap.core import cables_from_source

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.analysis import CharsetFilter, StemmingAnalyzer
from whoosh.writing import AsyncWriter
from whoosh.qparser import QueryParser
from whoosh import fields, sorting
from whoosh.support.charset import accent_map

fname = "/home/luiztheodoro/Documentos/mestrado/iri/trab_final/wikileaks-cables/cables.csv"

i = 0
for cable in cables_from_source(fname):
    print(cable.subject, cable.created)
    if i>5:
        break
    i += 1

atributos = [i for i in dir(cable) if not i.startswith('_')]
atributos.pop(3) #remove "classification_categories"
atributos.pop(4) #remove "comment"
print(atributos)

def build_doc(cable):
    doc = {}
    for a in atributos:
        try:
            if a == 'created':
                doc[a] = datetime.datetime.strptime(getattr(cable, a).strip(), "%Y-%m-%d %H:%M")
            else:
                doc[a] = getattr(cable, a)
        except AttributeError as e:
            print(e)
            doc[a] = ""
    return doc

def cable_doc_gen():
    """
    Função geradora que itera sobre cables.csv
    retornando um telegrama por vez, incluindo-o em um dicionário compatível com o elasticsearch.
    """
    for j,cable in enumerate(cables_from_source(fname)):
        doc = build_doc(cable)
        action = {
            "_index": "wikileaks",
            "_type": "telegramas",
            "_id": j,
            "doc": doc
            }
        if j == 1000: break
        if j%1000 == 0:
            print("Indexando telegrama número {}".format(j))
            
        yield action

schema = Schema(index = ID(stored=True), \
                cannonical_id = TEXT(stored=True), \
                content = TEXT(stored=True), \
                header = TEXT(stored=True), \
                classification = TEXT(stored=True), \
                subject = TEXT(stored=True), \
                origin = TEXT(stored=True), \
                created = DATETIME(stored=True), \
                tags = KEYWORD(stored=True))

index_path='/media/luiztheodoro/HD1T/mestrado/data/iri/indexdir'

os.mkdir(index_path)
ix = create_in(index_path, schema)

writer = ix.writer()
for j,cable in enumerate(cables_from_source(fname)):
    doc = build_doc(cable)
    writer.add_document(index=str(j), \
                        cannonical_id = doc['canonical_id'], \
                        content=str(doc["content"]), \
                        header=doc["header"], \
                        classification=doc["classification"], \
                        subject=doc["subject"], \
                        origin=doc["origin"], \
                        created=doc["created"], \
                        tags=" ".join(doc["tags"]))
    if j%1000 == 0: 
        print(j)
writer.commit()