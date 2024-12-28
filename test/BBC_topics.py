import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
dico = {}
dico_mois = {}
df = pd.read_csv('articles_bbc.csv')

date =  df.iloc[:, 2].tolist()
topics = df.iloc[:, 3].tolist()

for i in range(len(date)) : 
    if "ago" in date[i] : 
        print(date[i])
        date[i] = "x Dec 2024"
        print(date[i])
    if topics[i] != "['no_topics']" : 
        dico[date[i]] = topics[i]

print(dico)
print(len(dico))

for i in dico :
    dico[i] =  ast.literal_eval(dico[i])
    temp = i.split(" ")
    temp2 = temp[1:]
    temp = temp2[0] + " " + temp2[1]
    if temp in dico_mois : 
        dico_mois[temp] += dico[i]
    else : 
        dico_mois[temp] = dico[i]

for i in dico_mois : 
    liste = dico_mois[i]
    dico = {}
    for j in liste : 
        if j in dico : 
            dico[j] +=1
        else : 
            dico[j] = 1
    dico_mois[i] = dico
dico_2024 = {}
for i in dico_mois : 
    if "2023" in i :
        dico_2024[i] = dico_mois[i]
data = dico_2024
# Étape 1: Transformer les données
rows = []
for month, topics in data.items():
    for topic, count in topics.items():
        rows.append({'Month': month, 'Topic': topic, 'Count': count})

# Convertir en DataFrame
df = pd.DataFrame(rows)

# Ajouter le rang par mois (par nombre d'occurrences)
df['Rank'] = df.groupby('Month')['Count'].rank(method='first', ascending=False)

# Filtrer les sujets les plus populaires (Top 10 par exemple)
top_topics = df.groupby('Topic')['Count'].sum().nlargest(5).index
df_filtered = df[df['Topic'].isin(top_topics)]
month_order = [
    "Jan 2023", "Feb 2023", "Mar 2023", "Apr 2023", "May 2023", 
    "Jun 2023", "Jul 2023", "Aug 2023", "Sep 2023", "Oct 2023", 
    "Nov 2023", "Dec 2023"
]
df_filtered['Month'] = pd.Categorical(df_filtered['Month'], categories=month_order, ordered=True)
# Étape 2: Créer le Bump Chart
plt.figure(figsize=(12, 8))
sns.lineplot(
    data=df_filtered,
    x='Month',
    y='Rank',
    hue='Topic',
    marker='o'
)

# Inverser l'axe des rangs (1 = meilleur rang)
plt.gca().invert_yaxis()
plt.grid(True, linestyle='--', alpha=0.7)
# Ajouter des étiquettes et un titre
plt.title("évolution du ranking des sujets les plus utilisés durant l'année 2024 par la bbc", fontsize=16)
plt.xlabel('Mois', fontsize=12)
plt.ylabel('Rang', fontsize=12)
plt.legend(title='Sujets', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
# Ajouter des étiquettes pour chaque point
# Ajouter des étiquettes pour chaque point
for topic in top_topics:
    topic_data = df_filtered[df_filtered['Topic'] == topic]
    for _, row in topic_data.iterrows():
        plt.text(
            row['Month'], row['Rank'] - 0.3,  # Position verticale ajustée
            f"{int(row['Rank'])}",  # Étiquette indiquant le rang (converti en entier)
            fontsize=8, color='black', ha='center'
        )
        plt.text(
            row['Month'], row['Rank'] + 0.3,  # Position légèrement au-dessus pour le nom du sujet
            f"{row['Topic']}",  # Étiquette indiquant le nom du topic
            fontsize=7, color='black', ha='center', rotation=30  # Texte noir
        )


# Afficher le graphique
plt.show()

