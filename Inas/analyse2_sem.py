import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Charger le fichier JSON
with open("/cleaned2_text_corrected.json", "r") as file:
    data = json.load(file)

# Initialiser l'analyseur de sentiments VADER
analyser = SentimentIntensityAnalyzer()

# Créer un dictionnaire pour stocker les résultats
results = {}

# Parcourir les URL et leurs citations
for url, quotes in data.items():
    # Initialiser les valeurs d'analyse pour cette URL
    sentiment_summary = {
        "positive": 0,
        "neutral": 0,
        "negative": 0,
        "compound_scores": [],
        "average_compound": 0,
        "total_quotes": len(quotes),
    }

    # Analyser chaque citation
    for quote in quotes:
        scores = analyser.polarity_scores(quote)
        compound = scores["compound"]

        # Classifier la citation en fonction de son score compound
        if compound >= 0.5:
            sentiment_summary["positive"] += 1
        elif compound <= -0.5:
            sentiment_summary["negative"] += 1
        else:
            sentiment_summary["neutral"] += 1

        # Ajouter le score compound à la liste
        sentiment_summary["compound_scores"].append(compound)

    # Calculer la moyenne des scores compound
    if sentiment_summary["compound_scores"]:
        sentiment_summary["average_compound"] = sum(sentiment_summary["compound_scores"]) / len(
            sentiment_summary["compound_scores"]
        )

    # Ajouter les résultats pour cette URL
    results[url] = sentiment_summary

# Enregistrer les résultats dans un fichier JSON
output_filename = ".venv/AAsentiment_analysis_results.json"
with open(output_filename, "w") as output_file:
    json.dump(results, output_file, indent=4)

print(f"Sentiment analysis complete. Results saved to '{output_filename}'.")
