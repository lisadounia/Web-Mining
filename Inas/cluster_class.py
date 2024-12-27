import os
import pandas as pd
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

# Désactiver l'avertissement de huggingface/tokenizers
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Étape 1 : Lire le fichier Excel
file_path = "/Users/inasnanat/Documents/resultats_clusters.xlsx"  # Remplace par le chemin de ton fichier Excel
data = pd.read_excel(file_path)
subclasses = data['Subclass']  # Colonne contenant les subclasses

# Étape 2 : Convertir les subclasses en vecteurs sémantiques
print("Encodage des subclasses en vecteurs...")
model = SentenceTransformer('all-MiniLM-L6-v2')  # Modèle pour transformer les phrases en vecteurs
embeddings = model.encode(subclasses.tolist())  # Conversion des subclasses en vecteurs

# Étape 3 : Appliquer le clustering
print("Clustering des vecteurs...")
num_clusters = 30  # Nombre de clusters souhaités
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
clusters = kmeans.fit_predict(embeddings)

# Étape 4 : Obtenir le nom des clusters
print("Déterminer les noms des clusters...")
cluster_names = []
for i in range(num_clusters):
    # Trouver l'élément le plus proche du centre de chaque cluster
    cluster_center = kmeans.cluster_centers_[i]
    closest_idx = ((embeddings - cluster_center) ** 2).sum(axis=1).argmin()
    cluster_names.append(subclasses.iloc[closest_idx])

# Ajouter les noms des clusters dans le DataFrame
data['Cluster'] = [cluster_names[cluster] for cluster in clusters]

# Étape 5 : Remplacer manuellement certains noms de clusters
replacement_map = {
    "Quora": "report",
    "Aucun 'subclass of' trouvé sur la page Wikidata.": "other" # Remplace "quora" par "report" dans la colonne Cluster
}
data['Cluster'] = data['Cluster'].replace(replacement_map)

# Étape 6 : Sauvegarder les résultats dans un fichier Excel
output_file = "/Users/inasnanat/Documents/resultats3_clusters.xlsx"

# Vérifier que le répertoire de sortie existe, sinon le créer
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Sauvegarder le fichier Excel
print(f"Sauvegarde des résultats dans {output_file}...")
data.to_excel(output_file, index=False)

print("Clustering terminé. Résultats enregistrés avec succès !")



