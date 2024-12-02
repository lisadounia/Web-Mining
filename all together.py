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

dico = {}
mots_vides = list(set(stopwords.words('english'))) + ["'s"]
stem = nltk.stem.SnowballStemmer("english")


def extract(url):
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    soup_results = soup.select("div.mw-heading.mw-heading2 h2")
    sous_titres = [soup_result.text.strip() for soup_result in soup_results if
                   soup_result.text.strip().lower() not in ['see also', 'references', 'external links',
                                                            'further reading']]
    # print(sous_titres)
    contenu = ""
    soup_results1 = soup.select("p")
    for i in soup_results1:
        contenu += i.text
    # contenu = [soup_result1.text.strip() for soup_result1 in soup_results1]
    # print(contenu)
    h1 = (soup.select("h1"))
    h1 = h1[0].text
    return [h1, contenu]


def alllinks(url):
    dicosol = {}
    liste = []
    dico[extract(url)[0]] = extract(url)[1]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    allLinks = soup.select("p a")
    dicoliens = {}
    for link in allLinks:
        # Vérifier que le lien a un attribut 'href' et qu'il pointe vers un article wiki
        if link.has_attr('href') and link['href'].startswith("/wiki/"):
            liste.append(link['href'])
    liste = list(set(liste))
    for i in liste:
        new_url = "https://en.wikipedia.org" + i
        print(new_url)
        titre = extract(new_url)[0]
        dico[titre] = extract(new_url)[1]
        dicoliens[titre] = new_url
    return [dico, dicoliens]


def exctractcorpus(url):
    response = requests.get(url)
    response = response.content
    soup = BeautifulSoup(response, "html.parser")
    syn = soup.select("div[class='overview'] p")
    syn = syn[0].text
    return syn


def howmuchword(liste, mot):
    count = 0
    for i in liste:
        if i == mot:
            count += 1
    return count


def tdm(dico):
    ##transfomation des corpus en tokens
    listetotale = []
    for i in dico:
        dico[i] = dico[i].lower()
        dico[i] = nltk.word_tokenize(dico[i])
        tokens = dico[i]
        tokens = [token for token in tokens if token not in string.punctuation]
        tokens = [token for token in tokens if token not in mots_vides]
        tokens = [stem.stem(token) for token in tokens]
        listetotale += (tokens)
        dico[i] = tokens
    listeprov = listetotale
    listetotale = []
    for i in listeprov:
        if i in listetotale:
            continue
        listetotale.append(i)
    matrice = [[" "] + listetotale]
    for i in dico:
        liste = []
        liste.append(i)
        for j in listetotale:
            if j in dico[i]:
                liste.append(howmuchword(dico[i], j))
                continue
            liste.append(0)
        matrice.append(liste)
    df = pd.DataFrame(matrice)
    df.columns = df.iloc[0]
    df = df[1:]
    df.set_index(df.columns[0], inplace=True)
    # document_frequency = (df > 0).sum(axis=0)
    # filtered_td_matrix = df.loc[:, document_frequency >= 5]
    # document_frequency = (filtered_td_matrix > 0).sum(axis=0)
    # df = filtered_td_matrix.loc[:, document_frequency < 100]
    # Calcul du nombre total de documents
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
    filtered_td_matrix = df.loc[:, (document_frequency >= min_threshold) & (document_frequency <= max_threshold)]

    return filtered_td_matrix


def tfidf(df_input):
    row_sums = df_input.sum(axis=1)  # Total tokens per document (row)
    tf = df_input.div(row_sums, axis=0)
    df = (df_input > 0).sum(axis=0)  # Number of documents containing each term (column)
    N = df_input.shape[0]  # Number of documents
    idf = np.log((N) / (df))
    tf_idf = tf.mul(idf, axis=1)
    return (tf_idf)


def sim_mat(df_tf_idf):
    similarity_matrix = cosine_similarity(df_tf_idf)
    # Étape 2 : Convertir la matrice en DataFrame pour une meilleure lisibilité
    similarity_df = pd.DataFrame(similarity_matrix, index=df_tf_idf.index, columns=df_tf_idf.index)
    return (similarity_df)


def getsimilarlinks(url):
    dico = alllinks(url)[0]
    dicoliens = alllinks(url)[1]
    df = tdm(dico)
    dfvectorisé = tfidf(df)
    simmat = sim_mat(dfvectorisé)
    simmat = simmat.iloc[:, [0]]
    simmat = simmat.sort_values(by=simmat.columns[0], ascending=False)

    filtered_df = simmat[(simmat.iloc[:, 0] >= 0.10)]
    article_list = filtered_df.index.tolist()
    listeliens = []
    article_list = article_list[1:]
    for i in article_list:
        listeliens.append(dicoliens[i])

    return listeliens



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