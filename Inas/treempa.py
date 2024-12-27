import pandas as pd
import plotly.express as px

# Étape 1 : Charger le fichier Excel avec les clusters
file_path = "/Users/inasnanat/Documents/resultats3_clusters.xlsx"  # Chemin vers ton fichier Excel
data = pd.read_excel(file_path)

# Étape 2 : Calculer la fréquence de chaque cluster
cluster_counts = data['Cluster'].value_counts().reset_index()
cluster_counts.columns = ['Cluster', 'Count']  # Renommer les colonnes pour plus de clarté

# Étape 3 : Créer la treemap avec Plotly
fig = px.treemap(
    cluster_counts,
    path=['Cluster'],  # Chemin hiérarchique pour organiser les sections (ici, juste les clusters)
    values='Count',    # Taille des sections basée sur la fréquence
    title="Distribution des clusters dans une treemap",
    color='Count',     # Couleur en fonction de la fréquence
    color_continuous_scale='Viridis'  # Palette de couleurs (peut être modifiée)
)

# Étape 4 : Afficher la treemap
fig.show()
