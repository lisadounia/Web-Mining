import pandas as pd
import numpy as np
import pandas as pd
import json

# === Charger les données ===

cosine_matrix_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/local similarities /similarity_cosine.xlsx'
preference_matrix_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/local similarities /similarity_preferential_attachment.xlsx'
nodes_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/nodes.xlsx'

# # Charger les matrices
# cosine_matrix = pd.read_excel(cosine_matrix_path, index_col=0)
# preference_matrix = pd.read_excel(preference_matrix_path, index_col=0)
#
# # Charger le fichier nodes
# nodes_df = pd.read_excel(nodes_path)
# # Créer un dictionnaire qui mappe les indices aux noms
# node_mapping = nodes_df.set_index('Id')['Label'].to_dict()
#
#


# === Analyse Cosine Similarity ===

# # Collecter les paires avec un dictionnaire
# cosine_dict = []
# for i in range(len(cosine_matrix)):
#     for j in range(len(cosine_matrix)):
#         if i != j and cosine_matrix.iloc[i, j] > 0:  # Exclure auto-relations et valeurs <= 0
#             cosine_dict.append({
#                 'Node1': node_mapping.get(i, f'Node {i}'),
#                 'Node2': node_mapping.get(j, f'Node {j}'),
#                 'Cosine_Similarity': cosine_matrix.iloc[i, j]
#             })
#
# # Convertir en DataFrame
# cosine_pairs = pd.DataFrame(cosine_dict)
#
# # Supprimer les doublons symétriques
# cosine_pairs['Pair'] = cosine_pairs.apply(lambda row: frozenset([row['Node1'], row['Node2']]), axis=1)
# cosine_pairs = cosine_pairs.drop_duplicates(subset='Pair').drop(columns=['Pair'])
#
# # Trier par similarité décroissante
# cosine_pairs = cosine_pairs.sort_values(by='Cosine_Similarity', ascending=False)
#
# # === Exporter les résultats ===
#
# cosine_output_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Cosine_Analysis_Cleaned.xlsx'
# cosine_pairs.to_excel(cosine_output_path, index=False)
#
# # === Résumé des résultats ===
# print("Analyse Cosine Similarity :")
# print(cosine_pairs.head(10))
#
# print(f"\nLes résultats de l'analyse Cosine Similarity ont été exportés vers : {cosine_output_path}")
#

# === Analyse de l'Index de Préférence Attachée ===

# Collecter les paires avec un dictionnaire
# preference_dict=[]
# for i in range(len(preference_matrix)):
#     for j in range(len(preference_matrix)):
#         if i != j and preference_matrix.iloc[i, j] > 0:
#             preference_dict.append({
#                 'Node1': node_mapping.get(i, f'Node {i}'),
#                 'Node2': node_mapping.get(j, f'Node {j}'),
#                 'Preference_Index': preference_matrix.iloc[i, j]
#             })
#             print(f"Node1': {i} - 'Node2':  {j} - 'Preference_Index': {preference_matrix.iloc[i, j]}")
#
# # Convertir en DataFrame
# preference_pairs = pd.DataFrame(preference_dict)
#
# # Supprimer les doublons symétriques
# preference_pairs['Pair'] = preference_pairs.apply(lambda row: frozenset([row['Node1'], row['Node2']]), axis=1)
# preference_pairs = preference_pairs.drop_duplicates(subset='Pair').drop(columns=['Pair'])
#
# # Trier par index décroissant
# preference_pairs = preference_pairs.sort_values(by='Preference_Index', ascending=False)
#
# # === Exporter les résultats ===
#
# preference_output_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Preference_Analysis_Cleaned.xlsx'
# preference_pairs.to_excel(preference_output_path, index=False)
#
# print(f"Analyse Preference Attachment exportée vers : {preference_output_path}")

# # === Analyse combinée des deux similarités ===
# cosine_df = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Cosine_Analysis_Cleaned.xlsx')
# preference_df = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Preference_Analysis_Cleaned.xlsx')
#
# # Renommer les colonnes pour assurer la clarté
# cosine_df.rename(columns={'Cosine_Similarity': 'Cosine_Score'}, inplace=True)
# preference_df.rename(columns={'Preference_Index': 'Preference_Score'}, inplace=True)
#
# # Concaténer les deux DataFrames en utilisant un merge (union)
# combined_df = pd.merge(
#     cosine_df,
#     preference_df,
#     on=['Node1', 'Node2'],
#     how='outer'  # 'outer' pour inclure toutes les paires, même celles manquantes dans un des deux
# )
#
# # Remplacer les valeurs NaN par 0 pour les scores manquants
# combined_df['Cosine_Score'] = combined_df['Cosine_Score'].fillna(0)
# combined_df['Preference_Score'] = combined_df['Preference_Score'].fillna(0)
#
# # Trier les résultats pour faciliter l'analyse
# combined_df = combined_df.sort_values(by=['Cosine_Score', 'Preference_Score'], ascending=False)
#
# # Exporter le résultat combiné
# combined_df.to_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Combined_Analysis.xlsx', index=False)



# Charger le fichier Excel
excel_file = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/local similarities /Combined_Analysis.xlsx'
df = pd.read_excel(excel_file)

# Charger le fichier JSON contenant les clusters
clusters_file = '/Users/lisadounia/projets_masterQ1/Web-Mining/link analysis/dico_clusters_links'

with open(clusters_file, 'r') as f:
    clusters = json.load(f)

# Inverser les clusters pour une recherche rapide
node_to_cluster = {}
for cluster, nodes in clusters.items():
    for node in nodes:
        node_to_cluster[node] = cluster

# Ajouter les colonnes pour identifier les clusters et vérifier s'ils sont dans le même cluster
def assign_clusters(row):
    cluster1 = node_to_cluster.get(row['Node1'], 'Non trouvé')
    cluster2 = node_to_cluster.get(row['Node2'], 'Non trouvé')
    same_cluster = cluster1 == cluster2
    return pd.Series([cluster1, cluster2, same_cluster])

df[['Cluster1', 'Cluster2', 'Same_Cluster']] = df.apply(assign_clusters, axis=1)

# Sauvegarder le fichier Excel mis à jour
output_file = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/Combined_Analysis_with_Same_Cluster.xlsx'
df.to_excel(output_file, index=False)

print(f"Fichier mis à jour sauvegardé : {output_file}")