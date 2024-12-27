import json
import re

# Liste des mots-clés à exclure
EXCLUSION_KEYWORDS = [
    "chapter", "edition", "page", "pg.", "vol.", "volume", "no.", "part",
    "1.1ch", "ch.", "mai", "useandprivacy policy", "p.", "brown", "pp.", "quoted",
    "michael malice", "the new york times", "quotes", "the guardian"
]

# Liste des motifs regex à exclure
EXCLUSION_PATTERNS = [
    r"\b\d{4}\b",  # Années (ex : 2019)
    r"\b\w+\s\d{4}\b",  # Dates (ex : Mai 2019)
    r"\bpg\.\s?\d+\b",  # Pages (ex : pg. 12)
    r"\bvol(?:ume)?\.\s?\d+\b",  # Volumes (ex : Vol. 3 ou Volume 4)
    r"\bno\.\s?\d+\b",  # Numéros (ex : No. 5)
    r"\bpart\s\d+\b",  # Parties (ex : Part 2)
    r"\bchapter\b",  # Chapitres (ex : Chapter 4)
    r"useandprivacy policy"  # Mentions légales
]


# Fonction pour nettoyer une seule citation
def clean_quote(quote):
    # Vérifier si la citation contient un mot-clé d'exclusion
    for keyword in EXCLUSION_KEYWORDS:
        if keyword.lower() in quote.lower():
            return None

    # Vérifier si la citation correspond à un motif d'exclusion
    for pattern in EXCLUSION_PATTERNS:
        if re.search(pattern, quote, re.IGNORECASE):
            return None

    # Si aucun mot-clé ou motif d'exclusion n'est trouvé, retourner la citation nettoyée
    return quote.strip()


# Fonction pour traiter le dictionnaire
def clean_json(input_file, output_file):
    # Charger le fichier JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Nouveau dictionnaire pour les données nettoyées
    cleaned_data = {}

    # Parcourir chaque URL et liste de citations
    for url, quotes in data.items():
        cleaned_quotes = []
        for quote in quotes:
            # Nettoyer chaque citation
            cleaned_quote = clean_quote(quote)
            if cleaned_quote:  # Ajouter uniquement les citations valides
                cleaned_quotes.append(cleaned_quote)

        # Si toutes les citations sont supprimées, conserver au moins une citation originale
        if not cleaned_quotes and quotes:
            cleaned_quotes.append(quotes[0].strip())

        # Ajouter les citations nettoyées à l'URL correspondante
        if cleaned_quotes:
            cleaned_data[url] = cleaned_quotes

    # Enregistrer le fichier JSON nettoyé
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

    print(f"Fichier nettoyé enregistré dans {output_file}")


# Utilisation du script
input_file = 'clean_text.json'  # Chemin vers le fichier d'entrée
output_file = 'cleaned2_text.json'  # Chemin vers le fichier de sortie
clean_json(input_file, output_file)

