# Web-Mining
# Analyse Temporelle - Consignes d'Utilisation

## Objectif du Code
Ce code a pour objectif d'analyser l'historique d'un article fourni et de représenter, sous forme de graphique, l'évolution des tokens pertinents les plus fréquents sur une période déterminée.

## Utilisation du Code
1. Exécutez le script Python.
2. Lorsque le programme le demande, fournissez le lien de l'article à analyser.

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


