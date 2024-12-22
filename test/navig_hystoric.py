import numpy as np 
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
import spacy
from  nltk.corpus import stopwords
import requests
import pyLDAvis
import pyLDAvis.gensim
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
stopwords = stopwords.words("english")
dico_fréqeunce = {}
def link_to_corpus(url) :
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    corpus = soup.select("p")
    for i in range(len(corpus)) : 
        corpus[i] = corpus[i].text
    return corpus
    
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


url = "https://en.wikipedia.org/wiki/Social_inequality"
def rencoie_fréqeunces(url) : 
    dico_fréqeunce = {}
    corpus = link_to_corpus(url)
    corpus_liste = genwords(lemmatization(corpus))
    corpus = []
    for i in corpus_liste : 
        for j in i : 
            if j in stopwords : 
                continue
            corpus.append(j)

    for i in corpus : 
        if i not in dico_fréqeunce : 
            dico_fréqeunce[i] = 1
        else : 
            dico_fréqeunce[i]+= 1

    df_fréquences = pd.DataFrame(list(dico_fréqeunce.items()), columns=["token", "fréquence"])
    df_fréquences = df_fréquences.sort_values(by='fréquence', ascending=False)
    print(df_fréquences.head(5))
    return(dico_fréqeunce)
def send_historic (url) : 
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    liens = soup.select("h1")
    head = liens[0].text
    print(head)
    new_head = ""
    for i in head : 
        if i ==" " : 
            new_head+= "_"
            continue 
        new_head+= i

    new_url = "https://en.wikipedia.org/w/index.php?title="+new_head+"&action=history&offset=&limit=500"
    print(new_url)

    dico = {}

    response = requests.get(new_url)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")

    soup = soup.find(id="pagehistory")

    soupliste= soup.select("ul")
    liste_url = []
    for i in soupliste : 
        soup = i.find("bdi")
        soup = soup.find("a")

        url = "https://en.wikipedia.org/" +soup["href"]
        dico[soup.text] = url

    #df = pd.DataFrame(list(dico.items()), columns=["URL", "dates"])
    return dico


def dico_final(url,word) : 
    dico = send_historic(url) 
    dates = []
    for i in dico : 
        dates.append(i)


    dico_health = {}
    for i in range(0,len(dates),10) :
        clé = dates[i]
        date = clé 
        date = date.split(", ")
        date = date[1]

        dico_fréqeunce = rencoie_fréqeunces(dico[clé])
        fréquence = dico_fréqeunce[word]
        dico_health[date] = fréquence
    return dico_health
def illustrate(url) : 
    dico_fréqeunce = {}
    corpus = link_to_corpus(url)
    corpus_liste = genwords(lemmatization(corpus))
    corpus = []
    for i in corpus_liste : 
        for j in i : 
            if j in stopwords : 
                continue
            corpus.append(j)

    for i in corpus : 
        if i not in dico_fréqeunce : 
            dico_fréqeunce[i] = 1
        else : 
            dico_fréqeunce[i]+= 1

    df_fréquences = pd.DataFrame(list(dico_fréqeunce.items()), columns=["token", "fréquence"])
    df_fréquences = df_fréquences.sort_values(by='fréquence', ascending=False)
    ma_liste = df_fréquences.iloc[:, 0].tolist()
    ma_liste = ma_liste[:5]


    dico_health_1 = dico_final(url,ma_liste[0])
    dico_health_2 = dico_final(url,ma_liste[1])
    dico_health_3 = dico_final(url,ma_liste[2])
    dico_health_4 = dico_final(url,ma_liste[3])
    dico_health_5 = dico_final(url,ma_liste[4])

    data_dicts = [
        (dico_health_1, ma_liste[0]),
        (dico_health_2, ma_liste[1]),
        (dico_health_3, ma_liste[2]),
        (dico_health_4, ma_liste[3]),
        (dico_health_5, ma_liste[4])
    ]

    # Créer le graphique
    plt.figure(figsize=(12, 7))

    for data, label in data_dicts:
        # Conversion des clés en dates et tri
        dates = [datetime.strptime(date, "%d %B %Y") for date in data.keys()]
        frequencies = [data[date] for date in data.keys()]
        
        # Ajouter les données au graphique
        plt.plot(dates, frequencies, marker='o', linestyle='-', label=label)

    # Ajouter des étiquettes et un titre
    plt.xlabel("Durée")
    plt.ylabel("Fréquence")
    plt.title("Évolution des 5 mots les plus fréquents")

    # Ajouter une grille
    plt.grid(True, linestyle='--', alpha=0.6)

    # Améliorer la lisibilité de l'axe X
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d %b %Y"))
    plt.gcf().autofmt_xdate(rotation=45)

    # Ajouter la légende
    plt.legend()

    # Afficher le graphique
    plt.tight_layout()
    plt.show()

url = "https://en.wikipedia.org/wiki/Gender_equality"
illustrate(url)