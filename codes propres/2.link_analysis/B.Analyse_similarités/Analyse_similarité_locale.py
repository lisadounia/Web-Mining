import pandas as pd
import numpy as np
import pandas as pd
import json



cosine_matrix_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/local similarities /similarity_cosine.xlsx'
preference_matrix_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/local similarities /similarity_preferential_attachment.xlsx'
matrix_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/local similarities /similarity_common_neighbors.xlsx'
nodes_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/nodes.xlsx'

cosine_matrix = pd.read_excel(cosine_matrix_path, index_col=0)
preference_matrix = pd.read_excel(preference_matrix_path, index_col=0)
nodes_df = pd.read_excel(nodes_path)
common_neighbors_matrix = pd.read_excel(matrix_path, header=None).values
node_mapping = nodes_df.set_index('Id')['Label'].to_dict()




#### Analyse Cosine Similarity

# Liste où on met toutes les infos des paires ayant un cosine>0 dans un dico
cosine_dict = []
for i in range(len(cosine_matrix)):
    for j in range(len(cosine_matrix)):
        if i != j and cosine_matrix.iloc[i, j] > 0:
            cosine_dict.append({
                'Node1': node_mapping.get(i, f'Node {i}'),
                'Node2': node_mapping.get(j, f'Node {j}'),
                'Cosine_Similarity': cosine_matrix.iloc[i, j] })


cosine_pairs = pd.DataFrame(cosine_dict)

# Supprimer les doublons symétriques
cosine_pairs['Pair'] = cosine_pairs.apply(lambda row: frozenset([row['Node1'], row['Node2']]), axis=1)
cosine_pairs = cosine_pairs.drop_duplicates(subset='Pair').drop(columns=['Pair'])


cosine_pairs = cosine_pairs.sort_values(by='Cosine_Similarity', ascending=False)
cosine_output_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Cosine_Analysis_Cleaned.xlsx'
cosine_pairs.to_excel(cosine_output_path, index=False)



### Analyse de Préférence Attachée
# Liste où on met toutes les infos des paires ayant une préférence attaché >0 dans un dico
preference_dict=[]
for i in range(len(preference_matrix)):
    for j in range(len(preference_matrix)):
        if i != j and preference_matrix.iloc[i, j] > 0:
            preference_dict.append({
                'Node1': node_mapping.get(i, f'Node {i}'),
                'Node2': node_mapping.get(j, f'Node {j}'),
                'Preference_Index': preference_matrix.iloc[i, j] })


preference_pairs = pd.DataFrame(preference_dict)

# Supprimer les doublons symétriques
preference_pairs['Pair'] = preference_pairs.apply(lambda row: frozenset([row['Node1'], row['Node2']]), axis=1)
preference_pairs = preference_pairs.drop_duplicates(subset='Pair').drop(columns=['Pair'])

# Trier par index décroissant
preference_pairs = preference_pairs.sort_values(by='Preference_Index', ascending=False)
preference_output_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Preference_Analysis_Cleaned.xlsx'
preference_pairs.to_excel(preference_output_path, index=False)



#### Analyse combinée des deux similarités
cosine_df = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Cosine_Analysis_Cleaned.xlsx')
preference_df = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Preference_Analysis_Cleaned.xlsx')


cosine_df.rename(columns={'Cosine_Similarity': 'Cosine_Score'}, inplace=True)
preference_df.rename(columns={'Preference_Index': 'Preference_Score'}, inplace=True)

#  merge les df
combined_df = pd.merge(
    cosine_df,
    preference_df,
    on=['Node1', 'Node2'],
    how='outer' ) #  inclure toutes les paires, même celles manquantes dans un des deux



combined_df['Cosine_Score'] = combined_df['Cosine_Score'].fillna(0)
combined_df['Preference_Score'] = combined_df['Preference_Score'].fillna(0)


combined_df = combined_df.sort_values(by=['Cosine_Score', 'Preference_Score'], ascending=False)
combined_df.to_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Combined_Analysis.xlsx', index=False)



#Rajouter des colonnes pour identifier les clusters et vérifier s'ils sont dans le même cluster

#fichier avec les clusters
clusters_file = '/Users/lisadounia/projets_masterQ1/Web-Mining/link analysis/dico_clusters_links'
with open(clusters_file, 'r') as f:
    clusters = json.load(f)
node_to_cluster = {}
for cluster, nodes in clusters.items():
    for node in nodes:
        node_to_cluster[node] = cluster

def assign_clusters(row):
    cluster1 = node_to_cluster.get(row['Node1'], 'Non trouvé')
    cluster2 = node_to_cluster.get(row['Node2'], 'Non trouvé')
    same_cluster = cluster1 == cluster2
    return pd.Series([cluster1, cluster2, same_cluster])

combined_df[['Cluster1', 'Cluster2', 'Same_Cluster']] = combined_df.apply(assign_clusters, axis=1)

output_file = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Combined_Analysis_with_Same_Cluster.xlsx'
combined_df.to_excel(output_file, index=False)

### voisins communs


# Fonction pour trouver les clés des clusters de deux nœuds
def get_cluster_keys(node1, node2, clusters):
    node1_key, node2_key = None, None
    for cluster_key, cluster_nodes in clusters.items():
        if node1 in cluster_nodes:
            node1_key = cluster_key
        if node2 in cluster_nodes:
            node2_key = cluster_key
    return node1_key, node2_key

# Fonction pour trouver les paires de nœuds avec un seuil de voisins communs donné
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
min_common_neighbors = np.min(common_neighbors_matrix[common_neighbors_matrix > 0])
average_common_neighbors = np.mean(common_neighbors_matrix[common_neighbors_matrix > 0])
total_pairs_with_neighbors = (common_neighbors_matrix > 0).sum()



print(f"\nPaires avec plus de {threshold} voisins communs :")
print(f"Nombre total : {len(results)}")
for pair in results:
    if pair[3]:  # Dans le même cluster
        cluster_info = f"Dans le même cluster : {pair[4]}"
    else:  # Pas dans le même cluster
        cluster_info = f"Clusters différents : {pair[4]} (Node1) et {pair[5]} (Node2)"
    print(f"{pair[0]} - {pair[1]} : {pair[2]} voisins communs, {cluster_info}")


print(f"Maximum de voisins communs : {max_common_neighbors}")
print(f"Minimum de voisins communs (non nul) : {min_common_neighbors}")
print(f"Moyenne des voisins communs (non nul) : {average_common_neighbors:.2f}")
print(f"Total de paires avec voisins communs : {total_pairs_with_neighbors}")


output_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/pairs_common_neighbors_with_clusters.xlsx'
results_df = pd.DataFrame(results, columns=['Node1', 'Node2', 'CommonNeighbors', 'SameCluster', 'ClusterKeyNode1', 'ClusterKeyNode2'])
results_df.to_excel(output_path, index=False)

