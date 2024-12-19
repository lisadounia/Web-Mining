import pandas as pd
from bs4 import BeautifulSoup
import requests
import json

df = pd.read_excel("graph/edges.xlsx")
dico = {}

import pandas as pd


# Étape 1 : Récupérer la première colonne et la convertir en liste
colonnes_liens = df.iloc[:, 0].tolist()
colonnes_liens += df.iloc[:, 1].tolist()

# Étape 2 : Supprimer les doublons
Listes_liens = list(set(colonnes_liens))
count = 0 
for i in Listes_liens : 
    count += 1 
    response = requests.get(i)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    corpusliste = soup.select("p")
    corpus = ""
    for j in corpusliste : 
        corpus+= j.text
    dico[i] = corpus
    print(count)
    print(i)

print(dico)
print(len(dico))



# Chemin du fichier JSON
file_path = "wikipedia_corpus.json"

# Enregistrement du dictionnaire dans un fichier JSON
with open(file_path, "w", encoding="utf-8") as json_file:
    json.dump(dico, json_file, indent=4, ensure_ascii=False)

print(f"Dictionnaire enregistré dans le fichier {file_path}")
