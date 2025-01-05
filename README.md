# Web-Mining
# Analyse Temporelle - Consignes d'Utilisation

## Objectif du Code
Ce code a pour objectif d'analyser l'historique d'un article fourni et de représenter, sous forme de graphique, l'évolution des tokens pertinents les plus fréquents sur une période déterminée.

## Utilisation du Code
1. Exécutez le script Python.
2. Lorsque le programme le demande, fournissez le lien de l'article à analyser.

## Sources
le traitement des tokens de ce code s'inspire fortement de la vidéo suivante :
- [Tutoriel](https://www.youtube.com/watch?v=TKjjlp5_r7o)

## Packages à Installer
Avant d'exécuter le code, assurez-vous que les packages suivants sont installés. Vous pouvez les installer via `pip` si nécessaire.

- **numpy** : Calculs numériques
- **gensim** : Analyse de texte avancée
- **Spacy** : Traitement de langage naturel
- **NLTK** : (Natural Language Toolkit) pour l'analyse textuelle
- **requests** : Requêtes HTTP pour récupérer des données
- **PyLDAvis** : Visualisation des modèles de sujets (LDA)
- **BeautifulSoup (BS4)** : Scraping de données HTML
- **pandas** : Manipulation de données
- **matplotlib** : Création de graphiques
- **datetime** : Manipulation de dates et d'horaires



# Création Graphe - Consignes d'Utilisation

## Objectif du Code
Ce code permet de construire un graphe représentant la structure de Wikipédia à partir d'un article donné (par défaut : **Social Inequality**). Il explore les relations entre articles similaires sur deux niveaux d'exploration de Wikipédia. 

Les étapes principales incluent : 
1. Création d'une matrice **terme-document**.
2. Vectorisation de cette matrice.
3. Construction d'une matrice de similarité pour relier les articles.

## Utilisation du Code
1. Par défaut, le code commence avec l'article Wikipédia **Social Inequality**.
2. Si vous souhaitez changer le point de départ, modifiez la variable `start_url` située à la ligne 190 dans le script.
3. Exécutez le code pour générer le graphe de similarité.

## Packages à Installer
Assurez-vous que les packages suivants sont installés avant d'exécuter le code. Vous pouvez les installer via `pip` si nécessaire.

- **NLTK** : (Natural Language Toolkit) pour l'analyse textuelle.
- **requests** : Requêtes HTTP pour récupérer des données depuis Wikipédia.
- **BeautifulSoup (BS4)** : Scraping de données HTML.
- **pandas** : Manipulation de données.
- **scipy** : Calculs scientifiques pour construire la matrice de similarité.


# Collection_de_BBC - Consignes d'Utilisation

## Objectif du Code
Ce code parcourt les pages du site **BBC News** pour collecter les articles liés aux inégalités sociales, en enregistrant leurs dates, catégories, et autres informations pertinentes.

## Utilisation du Code
1. Exécutez le script Python.
2. Le programme générera automatiquement un fichier **CSV** contenant toutes les informations collectées.

## Packages à Installer
Assurez-vous que les packages suivants sont installés avant d'exécuter le code. Vous pouvez les installer via `pip` si nécessaire.

- **requests** : Pour récupérer les données depuis le site BBC News.
- **BeautifulSoup (BS4)** : Pour scraper et analyser les données HTML.
- **pandas** : Pour manipuler et sauvegarder les données dans un fichier CSV.

markdown
Copier le code
# BBC_ranking - Consignes d'Utilisation

## Objectif du Code
Ce code analyse le fichier généré par le script **Collection_de_BBC** pour établir un classement des termes les plus abordés au cours d'une année précise. Les résultats sont présentés sous forme d'un tableau évolutif.

## Utilisation du Code
1. Assurez-vous d'avoir exécuté le script **Collection_de_BBC** au préalable pour générer le fichier de données.
2. Exécutez ce script et fournissez :
   - Le nom du fichier CSV généré par **Collection_de_BBC**.
   - L'année à analyser.
3. Notez que les articles publiés avant 2023 sont moins catégorisés sur BBC News, ce qui peut affecter la qualité de l'analyse.

## Packages à Installer
Avant d'exécuter le code, installez les packages suivants via `pip` si nécessaire :

- **ast** : Manipulation des structures de données littérales en Python.
- **matplotlib** : Création de graphiques.
- **seaborn** : Visualisations statistiques avancées.
- **pandas** : Manipulation des données.

# Clustering - Consignes d'Utilisation

## Objectif du Code
Ce code utilise un fichier **CSV** contenant une liste de 100 liens Wikipédia en entrée et génère en sortie un fichier **HTML** représentant les différents clusters du corpus. Le modèle de clustering utilisé est l'**allocation latente de Dirichlet (LDA)**.

## Utilisation du Code
1. Préparez un fichier **CSV** contenant vos 100 liens Wikipédia.
2. Exécutez le script et fournissez le nom du fichier CSV lorsque le programme le demande.
3. Le script générera un fichier **HTML** que vous pourrez ouvrir dans n'importe quel navigateur pour visualiser les clusters.

## Sources
Ce code s'inspire fortement des deux vidéos suivantes :
- [Tutoriel 1](https://www.youtube.com/watch?v=TKjjlp5_r7o)
- [Tutoriel 2](https://www.youtube.com/watch?v=UEn3xHNBXJU&t=935s)

## Packages à Installer
Avant de lancer le script, assurez-vous que les packages suivants sont installés. Vous pouvez les installer avec `pip` si nécessaire :

- **numpy** : Calculs numériques.
- **gensim** : Analyse de texte avancée et modélisation thématique.
- **spacy** : Traitement de langage naturel.
- **nltk** : (Natural Language Toolkit) pour l'analyse textuelle.
- **requests** : Requêtes HTTP pour récupérer des données.
- **PyLDAvis** : Visualisation des modèles LDA.
- **BeautifulSoup (BS4)** : Scraping de données HTML.
- **pandas** : Manipulation de données.


# Co-occurrence - Consignes d'Utilisation

## Objectif du Code
Ce code prend un article Wikipédia en entrée et génère un tableau de co-occurrence des 5 tokens les plus fréquents dans l'article.

## Utilisation du Code
1. Lancez le script Python.
2. Fournissez le lien de l'article Wikipédia lorsque le programme le demande.
3. Le script analysera l'article et affichera un tableau de co-occurrence des tokens les plus fréquents.

## Sources
le traitement des tokens de ce code s'inspire fortement de la vidéo suivante :
- [Tutoriel](https://www.youtube.com/watch?v=TKjjlp5_r7o)


## Packages à Installer
Assurez-vous que les packages suivants sont installés avant d'exécuter le script. Vous pouvez les installer avec `pip` si nécessaire :

- **BeautifulSoup (BS4)** : Scraping de données HTML.
- **requests** : Requêtes HTTP pour récupérer des données.
- **pandas** : Manipulation de données.
- **numpy** : Calculs numériques.
- **gensim** : Analyse de texte avancée.
- **spacy** : Traitement de langage naturel.
- **nltk** : (Natural Language Toolkit) pour l'analyse textuelle.
- **PyLDAvis** : Visualisation des modèles thématiques (LDA).

# Word_cloud - Consignes d'Utilisation

## Objectif du Code
Ce code génère un **nuage de mots** (word cloud) basé sur les tokens les plus importants d'un article Wikipédia donné en entrée.

## Utilisation du Code
1. Fournissez un lien vers un article Wikipédia lorsque le programme le demande.
2. Si le lien est un lien Wikipédia standard, exécutez le code tel quel.
3. Si le lien provient de **Wikiquote**, remplacez le `"p"` par `"ul"` à la ligne 38 du script avant de l'exécuter.
4. Le code génèrera un nuage de mots des tokens les plus pertinents.

## Sources
le traitement des tokens de ce code s'inspire fortement de la vidéo suivante :
- [Tutoriel 1](https://www.youtube.com/watch?v=TKjjlp5_r7o)

La création du nuage de mot à été très fortement inspirée par la vidéo suivante : 

- [Tutoriel 2](https://www.youtube.com/watch?v=HcKUU5nNmrs)


## Packages à Installer
Avant d'exécuter le script, assurez-vous que les packages suivants sont installés. Vous pouvez les installer via `pip` si nécessaire :

- **BeautifulSoup (BS4)** : Scraping de données HTML.
- **requests** : Requêtes HTTP pour récupérer des données.
- **pandas** : Manipulation de données.
- **numpy** : Calculs numériques.
- **gensim** : Analyse de texte avancée.
- **spacy** : Traitement de langage naturel.
- **nltk** : (Natural Language Toolkit) pour l'analyse textuelle.
- **PyLDAvis** : Visualisation des modèles thématiques (LDA).
- **Wordcloud** : Génération de nuages de mots.

# Extraire_Subclass - Consignes d'Utilisation

## Objectif du Code
Ce code a pour objectif d'extraire les **sous-classes** associées à chaque article Wikipédia en se basant sur les données disponibles dans l'onglet Wikidata. Voici les étapes principales effectuées par le script :  
1. Transformation des liens Wikipédia du fichier Excel en liens Wikiquote.  
2. Extraction des sous-classes à partir des liens transformés.  
3. Ajout d'une nouvelle colonne intitulée **"subclass"** dans le fichier Excel original, contenant la sous-classe correspondant à chaque article Wikipédia.

## Utilisation du Code
1. Assurez-vous d'avoir le fichier **`nodes.xlsx`** généré dans la partie "Link Analysis".  
2. Exécutez le script Python.  
3. Le script transformera les liens, effectuera l'extraction des sous-classes, et mettra à jour le fichier Excel avec une colonne supplémentaire.  

## Packages à Installer
Avant d'exécuter le script, installez les packages suivants à l'aide de `pip` si nécessaire :  
- **requests** : Pour envoyer des requêtes HTTP aux serveurs.  
- **BeautifulSoup (BS4)** : Pour effectuer le scraping des données HTML.  
- **pandas** : Pour la manipulation et la mise à jour du fichier Excel.  


markdown
Copier le code
# Class_Wiki - Consignes d'Utilisation

## Objectif du Code
Ce code a pour objectif de regrouper les **sous-classes** issues du fichier Excel généré précédemment en **30 classes principales**. Cela permet de passer d'une granularité fine (sous-classes) à une classification plus générale.  
Une nouvelle colonne intitulée **"Classes"** sera ajoutée au fichier Excel, représentant la classification générale correspondant à chaque sous-classe.

## Utilisation du Code
1. Assurez-vous d'avoir le fichier Excel généré précédemment contenant les sous-classes.  
2. Exécutez le script Python.  
3. Le script analysera les sous-classes et les répartira dans l'une des 30 classes principales, en ajoutant une colonne **"Classes"** au fichier Excel.

## Packages à Installer
Avant d'exécuter le script, installez les packages suivants à l'aide de `pip` si nécessaire :  
- **pandas** : Pour manipuler les données du fichier Excel.  
- **scikit-learn** : Pour la classification des sous-classes en classes principales.  
- **SentenceTransformer** : Pour l'encodage des sous-classes en vecteurs permettant leur regroupement.  

# Treemap - Consignes d'Utilisation

## Objectif du Code
Ce code a pour objectif de générer une **treemap** des différentes classes associées à nos liens Wikipédia.  
La treemap offre une visualisation claire et intuitive de la répartition des classes, en mettant en évidence leur fréquence relative.

## Utilisation du Code
1. Assurez-vous de disposer d'un fichier contenant les classes associées à vos liens Wikipédia.  
2. Exécutez le script Python.  
3. Le script générera une **treemap** qui permettra d'observer la répartition des classes en fonction de leur fréquence.  

## Packages à Installer
Avant d'exécuter le script, installez les packages suivants à l'aide de `pip` si nécessaire :  
- **plotly_express** : Pour générer la treemap.  
- **pandas** : Pour manipuler les données en entrée.  


markdown
Copier le code
# Wikiquote - Consignes d'Utilisation

## Objectif du Code
Ce code exploite les **16 clusters** identifiés lors de la "link analysis" et sélectionne une **personnalité publique** représentative pour chacun de ces clusters. Voici les étapes principales du processus :  
1. À partir des liens Wikipédia des personnalités sélectionnées, le code génère leurs liens Wikiquote.  
2. Il accède à l'onglet Wikiquote correspondant et extrait uniquement le **corpus** de la page, c'est-à-dire leurs **citations** et **discours**, en excluant les titres, sous-titres, etc.  
3. Le contenu extrait est ensuite stocké dans un **dictionnaire** au format JSON, où chaque clé est l'URL Wikipédia de la personnalité, et chaque valeur contient l'ensemble de ses citations.

## Utilisation du Code
1. Assurez-vous d'avoir accès aux liens Wikipédia des personnalités publiques des 16 clusters identifiés.  
2. Exécutez le script Python.  
3. Le code générera un fichier JSON contenant les citations de chaque personnalité, organisées par leur URL Wikipédia.  

## Packages à Installer
Avant d'exécuter le script, installez les packages suivants à l'aide de `pip` si nécessaire :  
- **requests** : Pour récupérer le contenu HTML des pages Wikiquote.  
- **BeautifulSoup (BS4)** : Pour extraire le corpus à partir du code HTML des pages Wikiquote.  

# Texte_Nettoyage - Consignes d'Utilisation

## Objectif du Code
Ce code a pour objectif de **nettoyer les citations** précédemment extraites. Il supprime tous les éléments non pertinents, tels que :  
- Les sources  
- Les pages  
- Les dates  
- Les volumes  
- Les chapitres  
- Et d'autres informations inutiles.  

À l'issue du nettoyage, le script enregistre les citations nettoyées dans un nouveau fichier au format **JSON**.

## Utilisation du Code
1. Assurez-vous de disposer du fichier JSON contenant les citations brutes extraites à l'aide du script précédent.  
2. Exécutez le script Python.  
3. Le code nettoiera les citations et enregistrera les résultats dans un nouveau fichier JSON.  

## Packages à Installer
Avant d'exécuter le script, assurez-vous que les packages suivants sont installés :  
- **pandas** : Pour la manipulation des données structurées.  
- **json** : Pour lire et écrire les fichiers JSON. (Généralement inclus avec Python.)  

markdown
Copier le code
# Analyse_Semantique - Consignes d'Utilisation

## Objectif du Code
Ce code réalise une **analyse sémantique** basée sur le fichier JSON contenant les citations nettoyées. Voici les principales étapes effectuées par le script :  
1. Analyse de chaque citation pour chaque personne dans le fichier JSON, phrase par phrase.  
2. Calcul d'un **score sémantique** (compris entre -1 et 1) pour chaque phrase.  
3. Classification des citations en **positives**, **négatives**, ou **neutres**.  
4. Calcul du **score final** pour l'ensemble des citations de chaque personne, avec une évaluation du **caractère général** (positif, négatif ou neutre).  
5. Enregistrement des résultats dans un fichier **JSON** pour une analyse ultérieure.  

## Utilisation du Code
1. Assurez-vous de disposer du fichier JSON contenant les citations nettoyées.  
2. Exécutez le script Python.  
3. Le script analysera les citations et générera un fichier JSON contenant :  
   - Le nombre total de citations positives, négatives, ou neutres pour chaque personne.  
   - Le score final et le caractère général des citations de chaque personne.  

## Package à Installer
Avant d'exécuter le script, installez le package suivant à l'aide de `pip` si nécessaire :  
- **vaderSentiment** : Pour effectuer l'analyse sémantique des phrases.  
