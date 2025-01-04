import pandas as pd
import numpy as np

# === Charger les données ===

nodes_df = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/nodes.xlsx')
node_mapping = nodes_df.set_index('Id')['Label'].to_dict()

# === Étape 1 : Charger la matrice de transition ===
# Chemin vers la matrice de transition
transition_matrix_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/local similarities /random_walk_transition_matrix.xlsx'
transition_matrix = pd.read_excel(transition_matrix_path, header=None).values

#
# # Vérifier si la matrice est normalisée
# if not np.allclose(transition_matrix.sum(axis=1), 1):
#     print("Attention : La matrice de transition n'est pas normalisée.")
# else:
#     print("Matrice de transition correctement normalisée.")
#
# # === Étape 2 : Calculer la probabilité stationnaire ===
# # Calcul des valeurs propres et vecteurs propres
# eigenvalues, eigenvectors = np.linalg.eig(transition_matrix.T)
#
# # Trouver l'indice de la valeur propre 1 (ou très proche)
# stationary_index = np.argmin(np.abs(eigenvalues - 1))
#
# # Le vecteur propre correspondant donne la probabilité stationnaire
# stationary_vector = np.real(eigenvectors[:, stationary_index])
# stationary_vector = stationary_vector / stationary_vector.sum()  # Normaliser
#
# # Associer les valeurs aux noms des nœuds
# stationary_df = pd.DataFrame({
#     'Node': [node_mapping.get(i, f"Node {i}") for i in range(len(stationary_vector))],
#     'Stationary_Probability': stationary_vector
# })
#
# # Trier par probabilité décroissante
# stationary_df = stationary_df.sort_values(by='Stationary_Probability', ascending=False)
#
# # === Étape 3 : Exporter les résultats ===
#
# stationary_df.to_excel("/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/stationary_probabilities.xlsx", index=False)
#
# # Afficher les 10 nœuds les plus influents
# print("\nTop 10 des nœuds par probabilité stationnaire :")
# print(stationary_df.head(10))


import json
import pandas as pd

# === Charger les données ===
# Chemin vers le fichier JSON des clusters
clusters_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/analyse graph/dico_clusters_links'
stationary_probabilities_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/stationary_probabilities.xlsx'

# Charger les clusters
with open(clusters_path, 'r') as f:
    clusters = json.load(f)

# Charger les probabilités stationnaires
stationary_df = pd.read_excel(stationary_probabilities_path)

cluster_data = []
for cluster_id, nodes in clusters.items():
    for node in nodes:
        cluster_data.append({'Node': node, 'Cluster': cluster_id})

cluster_df = pd.DataFrame(cluster_data,index=False)
print(stationary_df.columns)
print(cluster_df.columns)


# Fusionner les clusters avec les probabilités stationnaires
merged_df = stationary_df.merge(cluster_df, on='Node', how='inner')

# === Calculer les sommes des probabilités stationnaires par cluster ===
cluster_probabilities = merged_df.groupby('Cluster')['Stationary_Probability'].sum().reset_index()

# Trier les clusters par probabilité décroissante
cluster_probabilities = cluster_probabilities.sort_values(by='Stationary_Probability', ascending=False)

# === Exporter les résultats ===
output_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/cluster_stationary_probabilities.xlsx'
cluster_probabilities.to_excel(output_path)

# === Afficher les résultats ===
print("\nSomme des probabilités stationnaires par cluster :")
print(cluster_probabilities)
