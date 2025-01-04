from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np 
import numpy as np 
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
import spacy
from  nltk.corpus import stopwords
import requests
import pyLDAvis
import pyLDAvis.gensim
stopwords = stopwords.words("english")
url = "https://en.wikipedia.org/wiki/Gender_equality"
response = requests.get(url)
content = response.text
soup = BeautifulSoup(content, "html.parser")
corpus = soup.select("p")
for i in range(len(corpus)) : 
    corpus[i] = corpus[i].text


def lemmatization (texts, allowed_posttags=["NOUN","ADJ","VERB","ADV"]): 
    nlp = spacy.load("en_core_web_sm",disable=["parser","ner"])
    texts_out = []
    for text in texts : 
        doc = nlp(text)
        new_text = []
        for token in doc : 
            if token.pos_ in allowed_posttags : 
                new_text.append(token.lemma_)
        final = " ".join(new_text)
        texts_out.append(final)
    return texts_out
def genwords(texts) : 
    final = []
    for text in texts : 
        new= gensim.utils.simple_preprocess(text,deacc=True)
        final.append(new)
    return final

liste_corpus = genwords(lemmatization(corpus)) 
corpus = []
for i in liste_corpus : 
    for j in i : 
        if j in stopwords : 
            continue
        corpus.append(j)

dico_fréquence = {}
for i in corpus : 
    if i not in dico_fréquence : 
        dico_fréquence[i] = 1
    else : 
        dico_fréquence[i]+= 1

df_fréquences = pd.DataFrame(list(dico_fréquence.items()), columns=["token", "fréquence"])
df_fréquences = df_fréquences.sort_values(by='fréquence', ascending=False)
print(df_fréquences.head(5))
ma_liste = df_fréquences.iloc[:, 0].tolist()
def cococcurence(first) : 
    dico_cooccurence = {}
    for i in range(len(corpus)) : 
        if corpus[i] == first : 
            avant = corpus[i-1]+"_"+first
            après = first+"_"+corpus[i+1]
            if avant in dico_cooccurence : 
                dico_cooccurence[avant] += 1 
            else : 
                dico_cooccurence[avant] = 1 
            if après in dico_cooccurence : 
                dico_cooccurence[après] += 1 
            else : 
                dico_cooccurence[après] = 1 
        

    df_cooccurence= pd.DataFrame(list(dico_cooccurence.items()), columns=["cooccurendce", "fréquence"])
    df_cooccurence = df_cooccurence.sort_values(by='fréquence', ascending=False)
    df_cooccurence   =  (df_cooccurence.head(5))
    ma_liste = df_cooccurence.iloc[:, 0].tolist()
    ma_liste = ma_liste[:5]
    fréquencesliste = []
    for i in ma_liste  : 
        i = str(i)
        temp = i.split("_")
        if temp[0] != first : 
            mot = temp[0]
        else : 
            mot = temp[1]
        fréquencesliste.append(dico_fréquence[mot])

    df_cooccurence["Fréquence du mot"] = fréquencesliste
    #df_cooccurence.to_excel(titre)
    print(df_cooccurence)


cococcurence(ma_liste[1])