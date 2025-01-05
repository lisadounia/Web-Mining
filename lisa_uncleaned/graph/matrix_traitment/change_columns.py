import pandas as pd 
from bs4 import BeautifulSoup
import requests
df  =pd.read_excel("adjacency_matrix_V2.xlsx")
noms_colonnes = df.columns.tolist()
noms_colonnes = noms_colonnes[1:]
liste = []
for i in noms_colonnes : 
    print(i)
    url = i
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    titre = soup.select('h1')[0]
    titre = titre.text
    liste.append(titre)
liste = [" "]+liste
df.columns = liste
liste = liste[1:]
# Changer les index
df.index = liste

df = df.iloc[:, 1:]
df.to_excel("nouvelle_matrice_V2.xlsx")