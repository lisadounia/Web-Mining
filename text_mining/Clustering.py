import numpy as np 
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import spacy
from  nltk.corpus import stopwords
import requests
import pyLDAvis
import pyLDAvis.gensim
from bs4 import BeautifulSoup
from gensim.models import TfidfModel
import json
import pandas as pd

file_path = "wikipedia_corpus.json"
listedescorpus = []
url =  "https://en.wikipedia.org/wiki/Social_inequality"
stopwords = stopwords.words("english")
def extract (url) :
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content,"html.parser")
    corpus = soup.select("p")
    for i in range(len(corpus)) : 
        corpus[i] = corpus[i].text
    corpusliste = corpus 
    corpus = ""
    for i in corpusliste : 
        corpus += i 
    return corpus
df = pd.read_csv("Top_100_Links_and_Page_Rankings.csv")
listedescorpus = df.iloc[:, 0].tolist()
listetemp = listedescorpus
listedescorpus = []
for i in range(100) : 
    print(i)
    listedescorpus.append(extract(listetemp[i]))

def lemmatization (texts, allowed_posttags=["NOUN","ADJ","VERB","ADV"]): 
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

datawords = genwords(lemmatization(listedescorpus))


# Générer les bigrammes et trigrammes
bigrams_phrases = gensim.models.Phrases(datawords, min_count=5, threshold=25)
trigrams_phrases = gensim.models.Phrases(bigrams_phrases[datawords], threshold=25)

bigram = gensim.models.phrases.Phraser(bigrams_phrases)
trigram = gensim.models.phrases.Phraser(trigrams_phrases)

# Fonctions pour créer les bigrammes et trigrammes
def make_biagrams(texts):
    return [bigram[doc] for doc in texts]

def make_triagrams(texts):
    return [trigram[doc] for doc in texts]

# Transformation
data_biagrams = make_biagrams(datawords)
data_biagrams_tragrams = make_triagrams(data_biagrams)
# Affichage d'un exemple
id2word = corpora.Dictionary(data_biagrams_tragrams)
texts = data_biagrams_tragrams
corpus = [id2word.doc2bow(text) for text in texts]


tfidf = TfidfModel(corpus,id2word = id2word)
low_value = 0.05
words = []
words_missings_in_tfidf = []
for i in range(0, len(corpus)):
    bow = corpus[i]
    low_value_words = [] #reinitialize to be safe. You can skip this.
    tfidf_ids = [id for id, value in tfidf[bow]]
    bow_ids = [id for id, value in bow]
    low_value_words = [id for id, value in tfidf[bow] if value < low_value]
    words_missing_in_tfidf = [id for id in bow_ids if id not in tfidf_ids] # The words with tf-idf socre 0 will be missing

    new_bow = [b for b in bow if b[0] not in low_value_words and b[0] not in words_missing_in_tfidf]     
    corpus[i] = new_bow
print()


lda_model  =gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=18,
                                            random_state=100,
                                            update_every=1,
                                            chunksize=100,
                                            passes=10,
                                            alpha="auto")
#pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda_model,corpus,id2word,mds="mmds",R=30)

pyLDAvis.save_html(vis, 'lda_visualization.html')

# Ouvrir dans le navigateur
import webbrowser
webbrowser.open('lda_visualization.html')
    