import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
dico = {}
dico_mois = {}

nom_fichier = input("Entrez le nom du fichier csv : ")
date_année = input("Entrez l'année que vous voulez analyser : ")
df = pd.read_csv(nom_fichier)

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
    if date_année in i :
        dico_2024[i] = dico_mois[i]
data = dico_2024
rows = []
for month, topics in data.items():
    for topic, count in topics.items():
        rows.append({'Month': month, 'Topic': topic, 'Count': count})
df = pd.DataFrame(rows)

df['Rank'] = df.groupby('Month')['Count'].rank(method='first', ascending=False)

top_topics = df.groupby('Topic')['Count'].sum().nlargest(5).index
df_filtered = df[df['Topic'].isin(top_topics)]
month_order = [
    "Jan "+date_année, "Feb "+date_année, "Mar "+date_année, "Apr "+date_année, "May "+date_année, 
    "Jun "+date_année, "Jul "+date_année, "Aug "+date_année, "Sep "+date_année, "Oct "+date_année, 
    "Nov "+date_année, "Dec "+date_année
]
df_filtered['Month'] = pd.Categorical(df_filtered['Month'], categories=month_order, ordered=True)

df['Rank'] = df.groupby('Month')['Count'].rank(method='first', ascending=False)

complete_index = pd.MultiIndex.from_product(
    [month_order, top_topics], names=['Month', 'Topic']
)
df_complete = df.set_index(['Month', 'Topic']).reindex(complete_index, fill_value=0).reset_index()

df_complete['Rank'] = df_complete.groupby('Month')['Count'].rank(method='first', ascending=False)

df_filtered = df_complete[df_complete['Topic'].isin(top_topics)]

plt.figure(figsize=(12, 8))
sns.lineplot(
    data=df_filtered,
    x='Month',
    y='Rank',
    hue='Topic',
    marker='o'
)

plt.gca().invert_yaxis()
plt.grid(True, linestyle='--', alpha=0.7)

plt.title("Évolution du ranking des sujets les plus utilisés durant l'année "+date_année+" par la BBC", fontsize=16)
plt.xlabel('Mois', fontsize=12)
plt.ylabel('Rang', fontsize=12)
plt.legend(title='Sujets', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

for topic in top_topics:
    topic_data = df_filtered[df_filtered['Topic'] == topic]
    for _, row in topic_data.iterrows():
        plt.text(
            row['Month'], row['Rank'] - 0.3,  
            f"{int(row['Rank'])}",  
            fontsize=8, color='black', ha='center'
        )
        plt.text(
            row['Month'], row['Rank'] + 0.3,  
            f"{row['Topic']}",  
            fontsize=7, color='black', ha='center', rotation=30
        )
plt.show()


