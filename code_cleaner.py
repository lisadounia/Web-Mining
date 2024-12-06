from bs4 import BeautifulSoup
import requests
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
import math
from collections import Counter
import string
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
mots_vides = list(set(stopwords.words('english'))) + ["'s"]
stem = nltk.stem.SnowballStemmer("english")
def howmuchword(liste, mot):
    count = 0
    for i in liste:
        if i == mot:
            count += 1
    return count

def similar_links(url) :
    liste_totale = [] 
    dicoliens = {}
    dicotokens = {}
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    liens = soup.select("p a")
    corpus = ""
    corpusliste = soup.select("p")
    for i in corpusliste : 
        corpus  += i.text
    tokens = corpus.lower()
    tokens = nltk.word_tokenize(tokens)
    tokens = [stem.stem(token)  # Étape 4 : appliquer le stemming
    for token in nltk.word_tokenize(corpus.lower())  # Étape 1 : mise en minuscule + tokenisation
    if token not in string.punctuation and token not in mots_vides  # Étapes 2 et 3 : suppression des ponctuations et mots vides
    ]
    liste_totale+=tokens
    dicoliens[soup.select('h1')[0]] = url
    dicotokens[soup.select('h1')[0]] = tokens
    for link in liens:
        if link.has_attr('href') and link['href'].startswith("/wiki/"):
            newurl = ("https://en.wikipedia.org"+link['href'])
            print(newurl)
            response = requests.get(newurl)
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            head = soup.select("h1")
            head = head[0].text
            if head not in dicoliens : 
                corpus = ""
                corpusliste = soup.select("p")
                for i in corpusliste : 
                    corpus += i.text 
                tokens = corpus.lower()
                tokens = nltk.word_tokenize(tokens)
                tokens = [stem.stem(token)  # Étape 4 : appliquer le stemming
                for token in nltk.word_tokenize(corpus.lower())  # Étape 1 : mise en minuscule + tokenisation
                if token not in string.punctuation and token not in mots_vides  # Étapes 2 et 3 : suppression des ponctuations et mots vides
                ]
                liste_totale+=tokens
                dicotokens[head] = tokens
                dicoliens[head] = newurl
    liste_totale = list(set(liste_totale))
    matrice = [[" "] + liste_totale]
    for i in dicotokens:
        liste = []
        liste.append(i)
        for j in liste_totale:
            if j in dicotokens[i]:
                liste.append(howmuchword(dicotokens[i], j))
                continue
            liste.append(0)
        matrice.append(liste)
    df = pd.DataFrame(matrice)
    df.columns = df.iloc[0]
    df = df[1:]
    df.set_index(df.columns[0], inplace=True)
    total_documents = df.shape[0]
    # Seuils en pourcentage
    min_percentage = 20  # Termes qui apparaissent dans moins de 5% des documents
    max_percentage = 80  # Termes qui apparaissent dans plus de 90% des documents
    # Calcul des seuils en nombre de documents
    min_threshold = min_percentage / 100 * total_documents
    max_threshold = max_percentage / 100 * total_documents
    # Calcul de la fréquence des documents
    document_frequency = (df > 0).sum(axis=0)
    # Filtrer les colonnes avec document_frequency >= 5% et < 90%
    df = df.loc[:, (document_frequency >= min_threshold) & (document_frequency <= max_threshold)]
    print(df)
    
similar_links("https://en.wikipedia.org/wiki/Social_inequality")