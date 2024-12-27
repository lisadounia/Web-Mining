import pandas as pd
import numpy as np
import json

# Charger la matrice des voisins communs
matrix_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/local similarities /similarity_common_neighbors.xlsx'
common_neighbors_matrix = pd.read_excel(matrix_path, header=None).values

# Charger le fichier des nœuds
nodes_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/nodes.xlsx'
nodes_df = pd.read_excel(nodes_path)

# Charger le fichier JSON des clusters
clusters_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/analyse graph/dico_clusters_links'
with open(clusters_path, 'r') as f:
    clusters = json.load(f)

# Créer un dictionnaire qui mappe les indices aux noms
node_mapping = nodes_df.set_index('Id')['Label'].to_dict()

# Fonction pour trouver les clés des clusters de deux nœuds
def get_cluster_keys(node1, node2, clusters):
    node1_key, node2_key = None, None
    for cluster_key, cluster_nodes in clusters.items():
        if node1 in cluster_nodes:
            node1_key = cluster_key
        if node2 in cluster_nodes:
            node2_key = cluster_key
    return node1_key, node2_key

# Fonction pour trouver les paires de nœuds avec un seuil donné
def find_pairs_with_common_neighbors(matrix, threshold, mapping, clusters):
    pairs = []
    n = matrix.shape[0]
    for i in range(n):
        for j in range(i + 1, n):  # Parcourt seulement la moitié supérieure de la matrice
            if matrix[i, j] > threshold:
                node1 = mapping.get(i, f'Node {i}')
                node2 = mapping.get(j, f'Node {j}')
                node1_key, node2_key = get_cluster_keys(node1, node2, clusters)
                in_same_cluster = node1_key == node2_key
                pairs.append((node1, node2, matrix[i, j], in_same_cluster, node1_key, node2_key))
    return pairs

# Trouver les paires avec plus de 3 voisins communs
threshold = 3
results = find_pairs_with_common_neighbors(common_neighbors_matrix, threshold, node_mapping, clusters)

# Statistiques globales
max_common_neighbors = np.max(common_neighbors_matrix)
min_common_neighbors = np.min(common_neighbors_matrix[common_neighbors_matrix > 0])  # Exclure les zéros
average_common_neighbors = np.mean(common_neighbors_matrix[common_neighbors_matrix > 0])  # Exclure les zéros
total_pairs_with_neighbors = (common_neighbors_matrix > 0).sum()

# Afficher les résultats
print("=== Analyse des voisins communs ===")

print(f"\nPaires avec plus de {threshold} voisins communs :")
print(f"Nombre total : {len(results)}")
for pair in results:
    if pair[3]:  # Dans le même cluster
        cluster_info = f"Dans le même cluster : {pair[4]}"
    else:  # Pas dans le même cluster
        cluster_info = f"Clusters différents : {pair[4]} (Node1) et {pair[5]} (Node2)"
    print(f"{pair[0]} - {pair[1]} : {pair[2]} voisins communs, {cluster_info}")

print("\n=== Statistiques globales ===")
print(f"Maximum de voisins communs : {max_common_neighbors}")
print(f"Minimum de voisins communs (non nul) : {min_common_neighbors}")
print(f"Moyenne des voisins communs (non nul) : {average_common_neighbors:.2f}")
print(f"Total de paires avec voisins communs : {total_pairs_with_neighbors}")

# Exporter les résultats dans un fichier Excel
output_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/pairs_common_neighbors_with_clusters.xlsx'
results_df = pd.DataFrame(results, columns=['Node1', 'Node2', 'CommonNeighbors', 'SameCluster', 'ClusterKeyNode1', 'ClusterKeyNode2'])
results_df.to_excel(output_path, index=False)
print(f"\nRésultats exportés vers : {output_path}")
