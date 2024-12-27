import pandas as pd
import networkx as nx
import numpy as np

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Charger la matrice d'adjacence
adj_matrix = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/adjacency_matrix_V2.xlsx', index_col=0)
print(f"Taille de la matrice d'adjacence : {adj_matrix.shape}")

# ================================
# Analyse des points d'articulation
# ================================
# Convertir en graphe non orienté (car les points d'articulation sont définis pour des graphes non orientés)
G = nx.from_pandas_adjacency(adj_matrix, create_using=nx.DiGraph)
G_undirected = G.to_undirected()
articulation_points = list(nx.articulation_points(G_undirected))
print("=== Points d'articulation ===")
print(f"Nombre total de points d'articulation : {len(articulation_points)}")


# Évaluer l'impact de chaque point d'articulation
impact_scores = []
for node in articulation_points:
    G_temp = G_undirected.copy()
    G_temp.remove_node(node)  # Supprimer le nœud
    components = list(nx.connected_components(G_temp))  # Trouver les composantes restantes
    largest_component_size = max(len(comp) for comp in components)  # Taille de la plus grande composante
    impact_scores.append((node, len(components), largest_component_size))

# Trier les points d'articulation par leur impact (nombre de composantes créées)
impact_scores = sorted(impact_scores, key=lambda x: (x[1], -x[2]), reverse=True)

# Top 5 points d'articulation critiques
top_5_articulation = impact_scores[:5]
print("\nTop 5 points d'articulation qui séparent les plus grandes composantes :")
for node, num_components, largest_size in top_5_articulation:
    print(f"Nœud {node} - Nombre de composantes après suppression : {num_components}, Taille de la plus grande composante : {largest_size}")

# ================================
# Analyse des ponts
# ================================

# Identifier les ponts
bridges = list(nx.bridges(G_undirected))
print("=== Ponts ===")
print(f"Nombre total de ponts : {len(bridges)}")

# Évaluer l'impact de chaque pont
bridge_impact_scores = []
for u, v in bridges:
    G_temp = G_undirected.copy()
    G_temp.remove_edge(u, v)  # Supprimer le pont
    components = list(nx.connected_components(G_temp))  # Trouver les composantes restantes
    largest_component_size = max(len(comp) for comp in components)  # Taille de la plus grande composante
    bridge_impact_scores.append(((u, v), len(components), largest_component_size))

# Trier les ponts par leur impact (nombre de composantes créées)
bridge_impact_scores = sorted(bridge_impact_scores, key=lambda x: (x[1], -x[2]), reverse=True)

# Top 5 ponts critiques
top_5_bridges = bridge_impact_scores[:5]
print("\nTop 5 ponts qui séparent les plus grandes composantes :")
for bridge, num_components, largest_size in top_5_bridges:
    print(f"Pont {bridge} - Nombre de composantes après suppression : {num_components}, Taille de la plus grande composante : {largest_size}")



# ================================
# Analyse des SCC (Strongly Connected Components)
# ================================
strongly_connected_components = list(nx.strongly_connected_components(G))
scc_sizes = [len(comp) for comp in strongly_connected_components]
sorted_scc = sorted(strongly_connected_components, key=len, reverse=True)
scc = sorted_scc[0]


# Supposons que le SCC le plus grand a été extrait
scc_nodes = sorted_scc[0]  # Le plus grand SCC
SCC = G.subgraph(scc_nodes).copy()  # Créer un sous-graphe pour ce SCC

# ================================
# 1. Informations générales
# ================================
print("===  Informations générales ===")
print(f"Taille du SCC : {len(SCC.nodes)} nœuds")
print(f"Nombre d'arêtes : {len(SCC.edges)}")
density = nx.density(SCC)
print(f"Densité du SCC : {density:.4f}")
