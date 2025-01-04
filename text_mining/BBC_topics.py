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
    if "2024" in i :
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
    "Jan 2024", "Feb 2024", "Mar 2024", "Apr 2024", "May 2024", 
    "Jun 2024", "Jul 2024", "Aug 2024", "Sep 2024", "Oct 2024", 
    "Nov 2024", "Dec 2024"
]
df_filtered['Month'] = pd.Categorical(df_filtered['Month'], categories=month_order, ordered=True)

# Calculer les rangs pour chaque mois (y compris les sujets non filtrés pour maintenir la cohérence des rangs)
df['Rank'] = df.groupby('Month')['Count'].rank(method='first', ascending=False)

# Remplir les mois et les rangs manquants pour les sujets sélectionnés
complete_index = pd.MultiIndex.from_product(
    [month_order, top_topics], names=['Month', 'Topic']
)
df_complete = df.set_index(['Month', 'Topic']).reindex(complete_index, fill_value=0).reset_index()

# Recalculer les rangs après remplissage
df_complete['Rank'] = df_complete.groupby('Month')['Count'].rank(method='first', ascending=False)

# Filtrer uniquement les sujets dans le top_topics
df_filtered = df_complete[df_complete['Topic'].isin(top_topics)]

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
plt.title("Évolution du ranking des sujets les plus utilisés durant l'année 2024 par la BBC", fontsize=16)
plt.xlabel('Mois', fontsize=12)
plt.ylabel('Rang', fontsize=12)
plt.legend(title='Sujets', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Ajouter des étiquettes pour chaque point
for topic in top_topics:
    topic_data = df_filtered[df_filtered['Topic'] == topic]
    for _, row in topic_data.iterrows():
        plt.text(
            row['Month'], row['Rank'] - 0.3,  # Position verticale ajustée
            f"{int(row['Rank'])}",  # Étiquette indiquant le rang
            fontsize=8, color='black', ha='center'
        )
        plt.text(
            row['Month'], row['Rank'] + 0.3,  # Position légèrement au-dessus pour le nom du sujet
            f"{row['Topic']}",  # Étiquette indiquant le nom du topic
            fontsize=7, color='black', ha='center', rotation=30
        )

# Afficher le graphique
plt.show()


