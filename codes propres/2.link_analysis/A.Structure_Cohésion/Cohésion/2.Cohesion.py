import pandas as pd
import networkx as nx
from collections import Counter
from networkx.algorithms.community import k_clique_communities


adj_matrix = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/adjacency_matrix_V2.xlsx', index_col=0)
G = nx.from_pandas_adjacency(adj_matrix, create_using=nx.DiGraph)
G_undirected = G.to_undirected()


#### informations générales
# ================================
print(f"Nombre de nœuds : {len(G.nodes)}")
print(f"Nombre d'arêtes : {len(G.edges)}")
density = nx.density(G)
print(f"Densité du graphe : {density:.4f}")
avg_shortest_path_length = nx.average_shortest_path_length(G_undirected)
print(f"Distance géodésique moyenne : {avg_shortest_path_length:.2f}")


### sous-groupes


#Cliques
print(f"\n========== Analyse des cliques ==============")
cliques = list(nx.find_cliques(G_undirected))
largest_clique = max(cliques, key=len)
sorted_cliques = sorted(cliques, key=len, reverse=True)  # Trier par taille décroissante

clique_sizes = [len(clique) for clique in cliques] # nombre de clique par taille
clique_count_by_size = Counter(clique_sizes)

print(f"Nombre total de cliques : {len(cliques)}")
print("\nNombre de cliques par taille :")
for size, count in sorted(clique_count_by_size.items(), reverse=True):
    print(f"- {count} cliques de taille {size}")

# Afficher les 3 plus grandes cliques avec leurs nœuds
print("\nTop 3 des plus grandes cliques :")
for i, clique in enumerate(sorted_cliques[:3], 1):  # Les 3 plus grandes cliques
    print(f"Clique {i} ({len(clique)} nœuds) : {clique}")




#n-cliques
for n in range(5, 6):
    count=0
    n_cliques = list(k_clique_communities(G_undirected, k=n))
    print(f"Nombre de{n}-cliques : {len(n_cliques)}")

    if n_cliques:
        for i, n_clique in enumerate(n_cliques, 1):
            print(f"{n}-clique {i} ({len(n_clique)} nœuds)")
            if len(n_clique)>0:
                count+=1
                first_n_clique = list(n_cliques[0])
                subgraph = G_undirected.subgraph(first_n_clique)
                sub_adj_matrix = nx.to_pandas_adjacency(subgraph)

                output_path = f"/Users/lisadounia/projets_masterQ1/Web-Mining/graph/subgraph_cohesions/{n}_clique_adjacency_matrix{count}.xlsx"
                sub_adj_matrix.to_excel(output_path)
                print(f"Matrice d'adjacence de la première {n}-clique exportée vers : {output_path}")

#Clan
for n in range(2, 7):
    print(f"\n=== Analyse des {n}-clans ===")
    n_clans = []
    for clique in nx.find_cliques(G_undirected):  # Cliques maximales
        if len(clique) >= 5:
            n_clans.append(clique)


    print(f"Nombre de {n}-clans : {len(n_clans)}")
    for i, clan in enumerate(n_clans, 1):
        print(f"{n}-clan {i} : {len(clan)} nœuds")

# k-Core
for k in range(2, 5):
    count=0
    k_core = nx.k_core(G_undirected, k=k)
    print(f"Nombre de nœuds dans le {k}-core : {len(k_core.nodes())}")
    if len(k_core.nodes()) > 0:
        count+=1
        k_core_adj_matrix = nx.to_pandas_adjacency(k_core)
        output_path = f"/Users/lisadounia/projets_masterQ1/Web-Mining/graph/{k}_core_adjacency_matrix{count}.xlsx"
        k_core_adj_matrix.to_excel(output_path)
        print(f"Matrice d'adjacence du {k}-core exportée vers : {output_path}")
