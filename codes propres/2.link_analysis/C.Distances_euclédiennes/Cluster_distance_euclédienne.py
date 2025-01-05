import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt
from itertools import combinations


data = pd.read_csv('/Users/lisadounia/projets_masterQ1/Web-Mining/link analysis/Linkclusters_info.csv')

# Calculer les centres des clusters
cluster_centers = data.groupby('modularity_class').agg({'X': 'mean', 'Y': 'mean'}).reset_index()

# Calculer les rayons maximaux pour chaque cluster
radii_max = []
for cluster in cluster_centers['modularity_class']:
    cluster_points = data[data['modularity_class'] == cluster]
    center_x = cluster_centers[cluster_centers['modularity_class'] == cluster]['X'].values[0]
    center_y = cluster_centers[cluster_centers['modularity_class'] == cluster]['Y'].values[0]
    distances = cluster_points.apply(
        lambda row: sqrt((row['X'] - center_x)**2 + (row['Y'] - center_y)**2),
        axis=1
    )
    radii_max.append(distances.max())

cluster_centers['Radius_Max'] = radii_max

# Normaliser les rayons pour éviter les tailles disproportionnées
max_radius = max(radii_max)
cluster_centers['Normalized_Radius'] = cluster_centers['Radius_Max'] / max_radius * 10  # Facteur de normalisation

# Créer le graphique
plt.figure(figsize=(12, 12))
plt.scatter(
    cluster_centers['X'],
    cluster_centers['Y'],
    s=cluster_centers['Normalized_Radius']**2,  # Taille proportionnelle au rayon normalisé
    alpha=0.5,
    c=cluster_centers['modularity_class'],
    cmap='tab10'
)

# Ajouter des annotations pour chaque cluster
for _, row in cluster_centers.iterrows():
    plt.text(row['X'], row['Y'], f'Cluster {int(row["modularity_class"])}', fontsize=9, ha='center')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Clusters Proportional to Their Extents')
plt.grid()
plt.show()

# Calculer les distances euclidiennes entre les clusters
distances = []
for (cluster_a, cluster_b) in combinations(cluster_centers['modularity_class'], 2):
    center_a = cluster_centers[cluster_centers['modularity_class'] == cluster_a][['X', 'Y']].values[0]
    center_b = cluster_centers[cluster_centers['modularity_class'] == cluster_b][['X', 'Y']].values[0]
    distance = sqrt((center_a[0] - center_b[0])**2 + (center_a[1] - center_b[1])**2)
    distances.append({'Cluster_A': cluster_a, 'Cluster_B': cluster_b, 'Distance': distance})

# Convertir en DataFrame
distance_df = pd.DataFrame(distances)
distance_df.to_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/link analysis/cluster_distances.xlsx')
print("Distances entre les clusters exportées.")



import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt
from itertools import combinations

# Charger les données
data = pd.read_csv('/Users/lisadounia/projets_masterQ1/Web-Mining/link analysis/Linkclusters_info.csv')

# Calculer les centres des clusters
cluster_centers = data.groupby('modularity_class').agg({'X': 'mean', 'Y': 'mean'}).reset_index()

# Calculer les rayons maximaux pour chaque cluster
radii_max = []
for cluster in cluster_centers['modularity_class']:
    cluster_points = data[data['modularity_class'] == cluster]
    center_x = cluster_centers[cluster_centers['modularity_class'] == cluster]['X'].values[0]
    center_y = cluster_centers[cluster_centers['modularity_class'] == cluster]['Y'].values[0]
    distances = cluster_points.apply(
        lambda row: sqrt((row['X'] - center_x)**2 + (row['Y'] - center_y)**2),
        axis=1
    )
    radii_max.append(distances.max())

cluster_centers['Radius_Max'] = radii_max

# normalisation les rayons pour éviter les tailles disproportionnées
max_radius = max(radii_max)
cluster_centers['Normalized_Radius'] = cluster_centers['Radius_Max'] / max_radius * 10  # Facteur de normalisation

# Créer le graphique
plt.figure(figsize=(12, 12))
plt.scatter(
    cluster_centers['X'],
    cluster_centers['Y'],
    s=cluster_centers['Normalized_Radius']**2,
    alpha=0.5,
    c=cluster_centers['modularity_class'],
    cmap='tab10'
)

# Ajouter des annotations pour chaque cluster
for _, row in cluster_centers.iterrows():
    plt.text(row['X'], row['Y'], f'Cluster {int(row["modularity_class"])}', fontsize=9, ha='center')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Clusters Proportional to Their Extents')
plt.grid()
plt.show()

# Calculer les distances euclidiennes entre les clusters
clusters = cluster_centers['modularity_class'].values
distance_matrix = pd.DataFrame(index=clusters, columns=clusters)

for (cluster_a, cluster_b) in combinations(clusters, 2):
    center_a = cluster_centers[cluster_centers['modularity_class'] == cluster_a][['X', 'Y']].values[0]
    center_b = cluster_centers[cluster_centers['modularity_class'] == cluster_b][['X', 'Y']].values[0]
    distance = sqrt((center_a[0] - center_b[0])**2 + (center_a[1] - center_b[1])**2)
    distance_matrix.loc[cluster_a, cluster_b] = distance
    distance_matrix.loc[cluster_b, cluster_a] = distance

# Remplir les diagonales avec 0 (distance d'un cluster à lui-même)
distance_matrix.fillna(0, inplace=True)

# Exporter la matrice de distances au format Excel
output_file = '/Users/lisadounia/projets_masterQ1/Web-Mining/link analysis/cluster_distance_matrix.xlsx'
distance_matrix.to_excel(output_file)
print(f"Matrice de distances entre les clusters exportée : {output_file}")

