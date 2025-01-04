
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from openpyxl.workbook import Workbook



def web_crawle1(start_link):
    response = requests.get(start_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    links_set = set()  # Utilisation d'un ensemble pour éviter les doublons
    soup_links= soup.find_all('a', href=True)
    for link in soup_links :  # Recherche toutes les balises <a> avec un attribut href
        href = link['href']  # Récupère la valeur de l'attribut href => lien
        # Filtre les liens : on ne garde que ceux qui pointent vers des articles Wikipédia
        if href.startswith \
                ('/wiki/') and ':' not in href:  # ':' pointent souvent vers des espaces de noms spécifiques (aide, catégories, fichiers) et non vers des articles standards.
            links_set.add("https://en.wikipedia.org" + href)  # Complète le lien relatif avec l'URL de base
    return links_set # Retourne les liens une fois la boucle terminée

def web_crawler(start_link):
    response = requests.get(start_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    links_set = set()  # Utilisation d'un ensemble pour éviter les doublons
    soup_links= soup.find_all('a', href=True)
    for link in soup_links :  # Recherche toutes les balises <a> avec un attribut href
        href = link['href']  # Récupère la valeur de l'attribut href => lien
        # Filtre les liens : on ne garde que ceux qui pointent vers des articles Wikipédia
        if href.startswith \
                ('/wiki/') and ':' not in href:  # ':' pointent souvent vers des espaces de noms spécifiques (aide, catégories, fichiers) et non vers des articles standards.
            links_set.add("https://en.wikipedia.org" + href)  # Complète le lien relatif avec l'URL de base
            if len(links_set )>=4 :
                return links_set
    return links_set

def add_url_mat(matrix, pages_list):
    # Ajouter une nouvelle colonne (valeurs 0) à chaque ligne existante
    for row in matrix:
        row.append(0)
    # Ajouter une nouvelle ligne (valeurs 0) pour la nouvelle page
    matrix.append([0] * len(pages_list))
    return matrix



def recursive_crawl(link, depth, pages_list, adjacency_matrix, visited,last_depth_neighbours):
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
    neighbors = web_crawler(link)
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

    last_depth_neighbours, pages_list, adjacency_matrix=recursive_crawl(start_link, depth, pages_list, adjacency_matrix, visited,last_depth_neighbours)
    adjacency_matrix=links_between_neighbours(last_depth_neighbours,pages_list, adjacency_matrix)

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



# faire en sorte de mettre les liens entre voisins
#faire en sorte qu'il analyse les x docs les plus pertinents (similaire a la current page) => voir avec Inas pour extraction texte et Cyril pour analyse de similarité textuelle

import nltk
nltk.download('punkt_tab')