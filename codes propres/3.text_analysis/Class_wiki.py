
import os
import pandas as pd
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

# Désactiver l'avertissement
os.environ["TOKENIZERS_PARALLELISM"] = "false"

file_path = "/Users/inasnanat/Documents/nodes_with_subclass.xlsx"
data = pd.read_excel(file_path)
subclasses = data['Subclass']

#Convertir les subclasses en vecteurs sémantiques
print("Encodage des subclasses en vecteurs...")
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(subclasses.tolist())

num_class = 30
kmeans = KMeans(n_clusters=num_class, random_state=42)
class1 = kmeans.fit_predict(embeddings)

class1_names = []
for i in range(num_class):
    class1_center = kmeans.cluster_centers_[i]
    closest_idx = ((embeddings - class1_center) ** 2).sum(axis=1).argmin()
    class1_names.append(subclasses.iloc[closest_idx])

data['Class'] = [class1_names[i] for i in class1]

replacement_map = {
    "Quora": "report",
    "Aucun 'subclass of' trouvé sur la page Wikidata.": "other"
}
data['Class'] = data['Class'].replace(replacement_map)

output_file = "/Users/inasnanat/Documents/resultats3_class.xlsx"

print(f"Sauvegarde des résultats dans {output_file}...")
data.to_excel(output_file, index=False)

print("Résultats enregistrés avec succès!")