import pandas as pd
import numpy as np
import json


# === Charger les données ===

nodes_df = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/nodes.xlsx')
node_mapping = nodes_df.set_index('Id')['Label'].to_dict()


transition_matrix_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/local similarities /random_walk_transition_matrix.xlsx'
transition_matrix = pd.read_excel(transition_matrix_path, header=None).values




# Calculer la probabilité stationnaire

eigenvalues, eigenvectors = np.linalg.eig(transition_matrix.T)
stationary_index = np.argmin(np.abs(eigenvalues - 1))

stationary_vector = np.real(eigenvectors[:, stationary_index])
stationary_vector = stationary_vector / stationary_vector.sum()

stationary_df = pd.DataFrame({
    'Node': [node_mapping.get(i, f"Node {i}") for i in range(len(stationary_vector))],
    'Stationary_Probability': stationary_vector
})


stationary_df = stationary_df.sort_values(by='Stationary_Probability', ascending=False)
stationary_df.to_excel("/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/stationary_probabilities.xlsx", index=False)



#Calculer les sommes des probabilités stationnaires par cluster
clusters_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/analyse graph/dico_clusters_links'
with open(clusters_path, 'r') as f:
    clusters = json.load(f)


cluster_data = []
for cluster_id, nodes in clusters.items():
    for node in nodes:
        cluster_data.append({'Node': node, 'Cluster': cluster_id})

cluster_df = pd.DataFrame(cluster_data,index=False)
merged_df = stationary_df.merge(cluster_df, on='Node', how='inner')


cluster_probabilities = merged_df.groupby('Cluster')['Stationary_Probability'].sum().reset_index()


cluster_probabilities = cluster_probabilities.sort_values(by='Stationary_Probability', ascending=False)
output_path = '/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/cluster_stationary_probabilities.xlsx'
cluster_probabilities.to_excel(output_path)
