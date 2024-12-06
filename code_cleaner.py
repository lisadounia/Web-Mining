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

def getsimilarlinks(url) :
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
    dicoliens[soup.select('h1')[0].text] = url
    dicotokens[soup.select('h1')[0].text] = tokens
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
    df_input = df.loc[:, (document_frequency >= min_threshold) & (document_frequency <= max_threshold)]
    row_sums = df_input.sum(axis=1)  # Total tokens per document (row)
    tf = df_input.div(row_sums, axis=0)
    df = (df_input > 0).sum(axis=0)  # Number of documents containing each term (column)
    print(df)
    N = df_input.shape[0]  # Number of documents
    idf = np.log((N) / (df))
    tf_idf = tf.mul(idf, axis=1)
    print(tf_idf)
    similarity_matrix = cosine_similarity(tf_idf)
    print(similarity_matrix)
    # Étape 2 : Convertir la matrice en DataFrame pour une meilleure lisibilité
    similarity_df = pd.DataFrame(similarity_matrix, index=tf_idf.index, columns=tf_idf.index)
    simmat = similarity_df.iloc[:, [0]]
    simmat = simmat.sort_values(by=simmat.columns[0], ascending=False)
    print(simmat)
    filtered_df = simmat[(simmat.iloc[:, 0] >= 0.30)]
    article_list = filtered_df.index.tolist()
    article_list = article_list[1:]
    liste = []
    for i in range(len(article_list)) : 
        print(str(i))
        print(article_list[i])
    for i in article_list : 
        liste.append(dicoliens[i])
    return liste
    
    
def recursive_crawl(link, depth, pages_list, adjacency_matrix, visited,last_depth_neighbours):
    print('in the recursive crawl')
    if depth == 0 or link in visited:
        return last_depth_neighbours,pages_list, adjacency_matrix

    # Marquer la page comme visitée
    visited.add(link)

    if link not in pages_list:
        pages_list.append(link)
        # Ajouter une nouvelle ligne et colonne à la matrice
        n = len(pages_list)
        for row in adjacency_matrix:
            row.append(0)
        adjacency_matrix.append([0] * n)

    # Obtenir les voisins de la page actuelle
    print('searching neighbours ')
    neighbors = getsimilarlinks(link)
    print(f"Exploring: {link}, Depth: {depth}, Neighbors: {len(neighbors)}")

    # Index de la page actuelle
    current_index = pages_list.index(link)

    for neighbor in neighbors:
        if neighbor not in pages_list:
            pages_list.append(neighbor)
            # Ajouter une nouvelle ligne et colonne à la matrice
            n = len(pages_list)
            for row in adjacency_matrix:
                row.append(0)
            adjacency_matrix.append([0] * n)
        if depth == 1 :
            last_depth_neighbours.add(neighbor)

        # Index du voisin
        neighbor_index = pages_list.index(neighbor)

        # Mettre à jour la matrice pour marquer la connexion
        adjacency_matrix[current_index][neighbor_index] = 1
        print(f"Added edge: {link} -> {neighbor}")

        # Appel récursif pour explorer les voisins
        last_depth_neighbours,pages_list, adjacency_matrix = recursive_crawl(neighbor, depth - 1, pages_list, adjacency_matrix, visited,last_depth_neighbours )

    return last_depth_neighbours,pages_list, adjacency_matrix

def links_between_neighbours(last_depth_neighbours, pages_list, adjacency_matrix):
    for page in last_depth_neighbours:
        # Obtenir les voisins de la page actuelle
        neighbors = web_crawler(page)

        current_index = pages_list.index(page)

        for neighbor in neighbors:
            if neighbor in pages_list:
                    # Trouver l'indice du voisin dans `pages_list`
                neighbor_index = pages_list.index(neighbor)

                    # Mettre à jour la matrice d'adjacence
                adjacency_matrix[current_index][neighbor_index] = 1

    return adjacency_matrix

def build_recursive_adjacency_matrix(start_link, depth=2):
    pages_list = []  # pages explorées
    adjacency_matrix = []  # Matrice d'adjacence
    visited = set()  # pages dejà pages visitées
    last_depth_neighbours = set()
    print('start crawling')
    last_depth_neighbours, pages_list, adjacency_matrix=recursive_crawl(start_link, depth, pages_list, adjacency_matrix, visited,last_depth_neighbours)
    adjacency_matrix=links_between_neighbours(last_depth_neighbours,pages_list, adjacency_matrix)
    print('crawling finish')
    adjacency_df = pd.DataFrame(adjacency_matrix, index=pages_list, columns=pages_list)
    return adjacency_df


if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/Social_inequality"
    depth = 2
    adjacency_df = build_recursive_adjacency_matrix(start_url, depth)

    # Afficher et sauvegarder les résultats
    print(adjacency_df)
    adjacency_df.to_excel("adjacency_matrix.xlsx")
    print("Done!")