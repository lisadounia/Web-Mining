from scipy.sparse import lil_matrix
from bs4 import BeautifulSoup
import requests
import nltk
import pandas as pd

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


def getsimilarlinks(url):
    liste_totale = []
    dicoliens = {}
    dicotokens = {}
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    liens = soup.select("p a")
    corpus = ""
    corpusliste = soup.select("p")
    for i in corpusliste:
        corpus += i.text
    tokens = corpus.lower()
    tokens = nltk.word_tokenize(tokens)
    tokens = [stem.stem(token)  
              for token in nltk.word_tokenize(corpus.lower())  
              if token not in string.punctuation and token not in mots_vides
              ]
    liste_totale += tokens
    dicoliens[soup.select('h1')[0].text] = url
    dicotokens[soup.select('h1')[0].text] = tokens
    for link in liens:
        if link.has_attr('href') and link['href'].startswith("/wiki/"):
            newurl = ("https://en.wikipedia.org" + link['href'])
            print(newurl)
            response = requests.get(newurl)
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            head = soup.select("h1")
            head = head[0].text
            if head not in dicoliens:
                corpus = ""
                corpusliste = soup.select("p")
                for i in corpusliste:
                    corpus += i.text
                tokens = corpus.lower()
                tokens = nltk.word_tokenize(tokens)
                tokens = [stem.stem(token) 
                          for token in nltk.word_tokenize(corpus.lower()) 
                          if token not in string.punctuation and token not in mots_vides
                          ]
                liste_totale += tokens
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
    min_percentage = 20  
    max_percentage = 80  
    min_threshold = min_percentage / 100 * total_documents
    max_threshold = max_percentage / 100 * total_documents
    document_frequency = (df > 0).sum(axis=0)
    df_input = df.loc[:, (document_frequency >= min_threshold) & (document_frequency <= max_threshold)]
    df_input.to_excel("matrice_tdm.xlsx")
    row_sums = df_input.sum(axis=1) 
    tf = df_input.div(row_sums, axis=0)
    df = (df_input > 0).sum(axis=0) 
    print(df)
    N = df_input.shape[0]  
    idf = np.log((N) / (df))
    tf_idf = tf.mul(idf, axis=1)
    tf_idf.to_excel("matrice_tf_idf.xlsx")
    print(tf_idf)
    similarity_matrix = cosine_similarity(tf_idf)
    
    print(similarity_matrix)
    similarity_df = pd.DataFrame(similarity_matrix, index=tf_idf.index, columns=tf_idf.index)
    similarity_df.to_excel("matrice_similarity.xlsx")
    simmat = similarity_df.iloc[:, [0]]
    simmat = simmat.sort_values(by=simmat.columns[0], ascending=False)
    print(simmat)
    filtered_df = simmat[(simmat.iloc[:, 0] >= 0.20)]
    article_list = filtered_df.index.tolist()
    article_list = article_list[1:]
    liste = []
    for i in range(len(article_list)):
        print(str(i))
        print(article_list[i])
    for i in article_list:
        liste.append(dicoliens[i])
    return liste


def recursive_crawl(link, depth, pages_list, adjacency_dict, visited, current_depth):
    #on analyse les liens de la derniere pronfondeur
    if current_depth > depth:
        return adjacency_dict
    if link in visited:
        return adjacency_dict

        # Marquer la page comme visitée
    visited.add(link)

    print("crawl of", link, "depth ", current_depth)
    if link not in pages_list:
        pages_list.append(link)

    # Obtenir les voisins de la page actuelle
    print('call fonction getsimilarlinks')
    neighbors = getsimilarlinks(link)
    print("got all the neighbours of ", link)

    # Ajouter les relations dans le dictionnaire
    if link not in adjacency_dict:
        adjacency_dict[link] = []

    #Analyse de chaque voisin de la page actuelle
    for neighbor in neighbors:
        if neighbor not in adjacency_dict[link]:
            adjacency_dict[link].append(neighbor)
        if neighbor not in pages_list:
            pages_list.append(neighbor)

        print(  link,"'s neighbours : ",adjacency_dict[link])
        # Appel récursif pour explorer le voisin
        adjacency_dict = recursive_crawl(neighbor, depth, pages_list, adjacency_dict, visited,current_depth + 1)


    return adjacency_dict


def build_recursive_adjacency_matrix(start_link, depth=2):
    print("building graph dynamically")
    pages_list = []  # Liste des pages explorées
    adjacency_dict = {}  # Dictionnaire pour stocker les relations
    visited=set()

    # Lancer la récolte des données récursive
    adjacency_dict = recursive_crawl(start_link, depth, pages_list, adjacency_dict,visited, current_depth=1)


    # Convertir en matrice creuse 
    n = len(pages_list)
    adjacency_matrix = lil_matrix((n, n), dtype=np.int8)

    for link, neighbors in adjacency_dict.items():
        current_index = pages_list.index(link)
        for neighbor in neighbors:
            neighbor_index = pages_list.index(neighbor)
            adjacency_matrix[current_index, neighbor_index] = 1
            print("link between", link, " and ", neighbor, " created")

    return adjacency_matrix, pages_list

if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/Social_inequality"
    depth = 2
    adjacency_matrix, pages_list = build_recursive_adjacency_matrix(start_url, depth)

    # Convertir la matrice creuse en un tableau
    dense_matrix = adjacency_matrix.toarray()

    df = pd.DataFrame(dense_matrix, index=pages_list, columns=pages_list)
    output_excel = "adjacency_matrix.xlsx"
    df.to_excel(output_excel, index=True)
    print(f"Adjacency matrix exported to {output_excel}")
