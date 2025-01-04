import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib
import spacy
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from wordcloud import WordCloud
mots_vides = list(set(stopwords.words('english'))) + ["'s"]
def lemmatization (texts, allowed_posttags=["NOUN","ADJ","ADV"]): 
    nlp = spacy.load("en_core_web_sm",disable=["parser","ner"])
    texts_out = []
    for text in texts : 
        doc = nlp(text)
        new_text = []
        for token in doc : 
            if token.pos_ in allowed_posttags : 
                new_text.append(token.lemma_)
        final = " ".join(new_text)
        texts_out.append(final)
    return texts_out

def genwords(texts) : 
    final = []
    for text in texts : 
        new= gensim.utils.simple_preprocess(text,deacc=True)
        final.append(new)
    return final


def wordcloud(url) : 
    corpus = ""
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content,"html.parser")
    corpus = soup.select("ul")
    for i in range(len(corpus)) : 
        corpus[i] = corpus[i].text
    listemots = genwords(lemmatization(corpus))
    listefinale = ""
    for i in listemots : 
        for j in i : 
            if j in mots_vides : 
                continue
            listefinale += j + " "
    wc = WordCloud(
    background_color='white',  # Couleur de fond
    stopwords=mots_vides,      # Liste des mots à ignorer
    height=600,
    width=800,                 # Plus large pour un meilleur ratio
    max_words=200,             # Nombre maximum de mots
    colormap='viridis',        # Palette de couleurs pour un rendu plus vif
    contour_width=0.5,         # Ajout d'un contour léger
    contour_color='black'      # Couleur du contour
    )
    wc.generate(listefinale)
    nom = "thomas_piketty.png"
    print(nom)
    wc.to_file(nom)

url = "https://en.wikiquote.org/wiki/Thomas_Piketty"

#df = pd.read_csv("Top_100_Links_and_Page_Rankings.csv")
#ma_liste = df.iloc[:, 0].tolist()
# for i in range(5) : 
  #  url = ma_liste[i]
   # nombre = i
    #print(url)
wordcloud(url)