import json
from textblob import TextBlob

# Charger le fichier JSON
with open('cleaned2_text_corrected.json', 'r') as file:
    data = json.load(file)


# Fonction pour analyser la polarité d'une citation
def analyse_sentiment(quote):
    # Créer un objet TextBlob
    blob = TextBlob(quote)
    # Retourner la polarité (entre -1 pour négatif et 1 pour positif)
    return blob.sentiment.polarity


# Fonction pour analyser les citations d'une URL et générer l'analyse
def analyser_citations_par_url(data):
    analyses = {}

    for url, citations in data.items():
        polarités = [analyse_sentiment(quote) for quote in citations]

        # Calculer la moyenne de la polarité
        moyenne_polarite = sum(polarités) / len(polarités) if polarités else 0

        # Déterminer si c'est positif, négatif ou neutre
        if moyenne_polarite > 0.1:
            sentiment = "Positif"
        elif moyenne_polarite < -0.1:
            sentiment = "Négatif"
        else:
            sentiment = "Neutre"

        # Ajouter l'analyse dans le dictionnaire
        analyses[url] = {
            "sentiment": sentiment,
            "moyenne_polarite": moyenne_polarite
        }

    return analyses


# Générer l'analyse pour toutes les URLs
analyses_resultat = analyser_citations_par_url(data)

with open('analyses_sentiment1.json', 'w') as outfile:
    json.dump(analyses_resultat, outfile, indent=2)

# Afficher ou sauvegarder le résultat
print(json.dumps(analyses_resultat, indent=2))

