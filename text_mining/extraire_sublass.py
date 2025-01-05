import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_wikidata_url(wikipedia_url):
    try:
        response = requests.get(wikipedia_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        wikidata_link = soup.find("link", {"rel": "alternate", "hreflang": "x-default"})
        if wikidata_link:
            return wikidata_link["href"]
        wikidata_tool_link = soup.find("a", {"href": lambda x: x and "www.wikidata.org/wiki/" in x})
        if wikidata_tool_link:
            return wikidata_tool_link["href"]
    except Exception as e:
        return None
    return None

def get_first_subclass_of(wikidata_url):
    try:
        response = requests.get(wikidata_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        first_subclass = soup.select_one('div.wikibase-snakview-value a[title^="Q"]')
        return first_subclass.text.strip() if first_subclass else None
    except Exception as e:
        return None

def extract_first_subclass(wikipedia_url):
    wikidata_url = get_wikidata_url(wikipedia_url)
    first_subclass = get_first_subclass_of(wikidata_url)
    if not first_subclass:
        return "Aucun 'subclass of' trouvé sur la page Wikidata."
    return first_subclass

def process_excel(file_path):
    df = pd.read_excel(file_path)
    if 'Label' not in df.columns:
        raise ValueError("La colonne 'Label' n'existe pas dans le fichier Excel.")

    df['Subclass'] = df['Label'].apply(extract_first_subclass)
    output_file = file_path.replace('.xlsx', '_with_subclass.xlsx')
    df.to_excel(output_file, index=False)
    print(f"Résultats enregistrés dans : {output_file}")

file_path = '/Users/inasnanat/code/nodes.xlsx'
process_excel(file_path)