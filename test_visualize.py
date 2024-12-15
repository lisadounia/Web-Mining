import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Charger la matrice d'adjacence depuis le fichier Excel
def load_adjacency_matrix(file_path):
    """
    Charge la matrice d'adjacence depuis un fichier Excel.
    
    Args:
    file_path (str): Chemin vers le fichier Excel
    
    Returns:
    pandas.DataFrame: Matrice d'adjacence
    """
    # Lit le premier onglet du fichier Excel
    df = pd.read_excel(file_path)
    
    return df

# Convertir la matrice en graphe NetworkX
def create_graph_from_matrix(matrix):
    """
    Convertit une matrice d'adjacence en graphe NetworkX
    
    Args:
    matrix (pandas.DataFrame): Matrice d'adjacence
    
    Returns:
    networkx.Graph: Graphe créé à partir de la matrice
    """
    # Crée un graphe non dirigé
    G = nx.Graph()
    
    # Ajoute les nœuds
    nodes = matrix.columns.tolist()
    G.add_nodes_from(nodes)
    
    # Ajoute les arêtes
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if matrix.iloc[i, j] > 0:  # Vous pouvez ajuster ce seuil si nécessaire
                G.add_edge(nodes[i], nodes[j], weight=matrix.iloc[i, j])
    
    return G

# Visualiser le graphe
def visualize_graph(G):
    """
    Visualise le graphe avec différentes options
    
    Args:
    G (networkx.Graph): Graphe à visualiser
    """
    plt.figure(figsize=(12, 8))
    
    # Layout avec spring pour un placement automatique des nœuds
    pos = nx.spring_layout(G, k=0.5)  # k contrôle l'espacement
    
    # Dessiner les nœuds
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                           node_size=300, alpha=0.8)
    
    # Dessiner les arêtes
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.5)
    
    # Ajouter les étiquettes des nœuds
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    
    plt.title("Visualisation du Graphe à partir de la Matrice d'Adjacence")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Exemple d'utilisation
def main(file_path):
    """
    Fonction principale pour charger, créer et visualiser le graphe
    
    Args:
    file_path (str): Chemin vers le fichier Excel contenant la matrice d'adjacence
    """
    # Charger la matrice
    matrix = load_adjacency_matrix(file_path)
    
    # Créer le graphe
    G = create_graph_from_matrix(matrix)
    
    # Visualiser le graphe
    visualize_graph(G)

main("adjacency_matrix.xlsx")