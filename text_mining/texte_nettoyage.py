import json
import re

EXCLUSION_KEYWORDS = ["chapter", "edition", "page", "pg.", "vol.", "volume", "no.", "part",
    "1.1ch", "ch.", "mai", "useandprivacy policy", "p.", "brown", "pp.", "quoted",
    "michael malice", "the new york times", "quotes", "the guardian"]

EXCLUSION_PATTERNS = [r"\b\d{4}\b", r"\b\w+\s\d{4}\b", r"\bpg\.\s?\d+\b", r"\bvol(?:ume)?\.\s?\d+\b",
    r"\bno\.\s?\d+\b",  r"\bpart\s\d+\b",  r"\bchapter\b", r"useandprivacy policy"]

def clean_quote(quote):
    for keyword in EXCLUSION_KEYWORDS:
        if keyword.lower() in quote.lower():
            return None
    for pattern in EXCLUSION_PATTERNS:
        if re.search(pattern, quote, re.IGNORECASE):
            return None
    return quote.strip()

def clean_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cleaned_data = {}
    for url, quotes in data.items():
        cleaned_quotes = []
        for quote in quotes:
            cleaned_quote = clean_quote(quote)
            if cleaned_quote:
                cleaned_quotes.append(cleaned_quote)
        if not cleaned_quotes and quotes:
            cleaned_quotes.append(quotes[0].strip())
        if cleaned_quotes:
            cleaned_data[url] = cleaned_quotes

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

    print(f"Fichier nettoyé enregistré dans {output_file}")


input_file = 'clean_text.json'
output_file = 'cleaned2_text.json'
clean_json(input_file, output_file)
