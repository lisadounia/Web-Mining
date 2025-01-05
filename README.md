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

### Exemple de commande pour installer tous les packages :
```bash
pip install numpy gensim spacy nltk requests pyldavis beautifulsoup4 pandas matplotlib
# La commande ci-dessus installe tous les packages nécessaires pour l'analyse temporelle.

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

### Exemple de commande pour installer tous les packages :
```bash
pip install nltk requests beautifulsoup4 pandas scipy
# La commande ci-dessus installe les packages nécessaires pour la création de graphe.
