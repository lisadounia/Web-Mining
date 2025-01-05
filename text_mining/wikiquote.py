wikipedia_url = ["https://en.wikipedia.org/wiki/Thomas_Piketty", "https://en.wikipedia.org/wiki/Ludwig_von_Mises",
                 "https://en.wikipedia.org/wiki/Alfred_Marshall", "https://en.wikipedia.org/wiki/Joseph_Schumpeter",
                 "https://en.wikipedia.org/wiki/Jason_Hickel","https://en.wikipedia.org/wiki/Anthony_Giddens",
                 "https://en.wikipedia.org/wiki/Karl_Marx", "https://en.wikipedia.org/wiki/Michel_Foucault",
                 "https://en.wikipedia.org/wiki/Charles_V._Hamilton", "https://en.wikipedia.org/wiki/Susan_Brownmiller",
                 "https://en.wikipedia.org/wiki/Marilyn_Frye", "https://en.wikipedia.org/wiki/Bill_Clinton",
                 "https://en.wikipedia.org/wiki/Michelle_Alexander", "https://en.wikipedia.org/wiki/Lyndon_B._Johnson",
                 "https://en.wikipedia.org/wiki/Jimmy_Carter","https://en.wikipedia.org/wiki/Bill_Gates"]

import requests
def get_wikiquote_urls(wikipedia_urls):
    results = {}
    for i in wikipedia_urls:
        if "wikipedia.org/wiki/" in i:
            title = i.split("wikipedia.org/wiki/")[1]
            wikiquote_url = f"https://en.wikiquote.org/wiki/{title}"
            results[i] = wikiquote_url
    return results

wikiquote_urls = get_wikiquote_urls(wikipedia_url)
print(wikiquote_urls)

import requests
from bs4 import BeautifulSoup
import re
import json

def extract_clean_text_from_wikiquote(urls):
    extracted_text = {}
    for name, url in urls.items(): #nettoyage
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        clean_phrases = []
        for li in soup.select("ul > li"):
            for sup in li.select("sup"):
                sup.extract()
            text = li.get_text(strip=True)
            if "QuotesToggle Quotes subsection" in text:
                continue
            text = re.sub(r"\(.*?\)|\[.*?\]|\{.*?\}", "", text)
            text = text.strip()
            if len(text) > 50:
                clean_phrases.append(text)
        extracted_text[name] = clean_phrases
    return extracted_text

clean_text = extract_clean_text_from_wikiquote(wikiquote_urls)

with open("clean_text.json", "w", encoding="utf-8") as f:
    json.dump(clean_text, f, ensure_ascii=False, indent=4)

print("Les résultats sont enregistrés dans 'clean_text.json'.")