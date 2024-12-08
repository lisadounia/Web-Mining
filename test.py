import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def visualize_graph(adjacency_matrix_file, max_nodes=50):
    # Charger le fichier Excel dans un DataFrame
    df = pd.read_excel(adjacency_matrix_file, index_col=0)

    # Créer un graphe dirigé avec NetworkX
    G = nx.DiGraph()

    # Ajouter les nœuds et les arêtes
    nodes = df.index.tolist()  # Liste des noms des pages
    adjacency_matrix = df.to_numpy()

    for i, source in enumerate(nodes):
        for j, target in enumerate(nodes):
            if adjacency_matrix[i, j] > 0:  # S'il y a un lien
                G.add_edge(source, target)

    # Limiter le nombre de nœuds pour un graphe clair
    if max_nodes and len(G.nodes) > max_nodes:
        G = G.subgraph(list(G.nodes)[:max_nodes])

    # Générer les positions des nœuds
    pos = nx.spring_layout(G, seed=42)

    # Dessiner le graphe
    plt.figure(figsize=(12, 12))
    nx.draw(
        G, pos,
        with_labels=True,
        node_size=500,
        node_color="lightblue",
        font_size=8,
        font_color="black",
        arrowstyle="->",
        arrowsize=15
    )
    plt.title("Graph Visualization")
    plt.show()

input_excel = "adjacency_matrix.xlsx"
visualize_graph(input_excel)