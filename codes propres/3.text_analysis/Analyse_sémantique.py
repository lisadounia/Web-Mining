import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

with open("cleaned2_text_corrected.json", "r") as file:
    data = json.load(file)

analyser = SentimentIntensityAnalyzer()

results = {}

for url, quotes in data.items():
    sentiment_summary = {"positive": 0, "neutral": 0, "negative": 0, "compound_scores": [], "average_compound": 0, "total_quotes": len(quotes),}
    for quote in quotes:
        scores = analyser.polarity_scores(quote)
        compound = scores["compound"]
        if compound >= 0.5:
            sentiment_summary["positive"] += 1
        elif compound <= -0.5:
            sentiment_summary["negative"] += 1
        else:
            sentiment_summary["neutral"] += 1
        sentiment_summary["compound_scores"].append(compound)

    if sentiment_summary["compound_scores"]:
        sentiment_summary["average_compound"] = sum(sentiment_summary["compound_scores"]) / len(sentiment_summary["compound_scores"])

    results[url] = sentiment_summary

output_filename = ".venv/resultats_analyse_semantique.json"
with open(output_filename, "w") as output_file:
    json.dump(results, output_file, indent=4)

print(f"Sentiment analysis complete. Results saved to '{output_filename}'.")