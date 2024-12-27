import pandas as pd
import networkx as nx
from networkx.algorithms.community import k_clique_communities

# Charger la matrice d'adjacence
adj_matrix = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/adjacency_matrix_V2.xlsx', index_col=0)
print(f"Taille de la matrice d'adjacence : {adj_matrix.shape}")

# Créer un graphe dirigé
G = nx.from_pandas_adjacency(adj_matrix, create_using=nx.DiGraph)

# Convertir en graphe non orienté
G_undirected = G.to_undirected()

# ================================
# 1. Informations générales
# ================================
print(f"Nombre de nœuds : {len(G.nodes)}")
print(f"Nombre d'arêtes : {len(G.edges)}")
density = nx.density(G)
print(f"Densité du graphe : {density:.4f}")

# Calculer le diamètre
diameter = nx.diameter(G_undirected)
print(f"Diamètre du graphe : {diameter}")

# Distance géodésique moyenne
if len(G_undirected) > 1:
    avg_shortest_path_length = nx.average_shortest_path_length(G_undirected)
    print(f"Distance géodésique moyenne : {avg_shortest_path_length:.2f}")

# ================================
# 2. Sous-groupes
# ================================

# (a) Cliques
print(f"\n========== Analyse des cliques ==============")
cliques = list(nx.find_cliques(G_undirected))  # Trouver toutes les cliques maximales
largest_clique = max(cliques, key=len)
sorted_cliques = sorted(cliques, key=len, reverse=True)[:3]  # Les 3 plus grandes cliques

print(f"Nombre total de cliques : {len(cliques)}")
print(f"La plus grande clique contient {len(largest_clique)} nœuds : {largest_clique}")
print("Top 3 des plus grandes cliques :")
for i, clique in enumerate(sorted_cliques, 1):
    print(f"Clique {i}({len(clique)} nœuds) ")

# (b) n-Cliques
for n in range(2, 5):
    count=0
    print(f"\n=== Analyse des {n}-cliques ===")
    n_cliques = list(k_clique_communities(G_undirected, k=n))
    print(f"Nombre de communautés {n}-cliques : {len(n_cliques)}")

    if n_cliques:
        for i, n_clique in enumerate(n_cliques, 1):
            print(f"{n}-clique {i} ({len(n_clique)} nœuds)")
            if len(n_clique)>0:
                count+=1
                # Exporter la première n-clique en matrice d'adjacence
                first_n_clique = list(n_cliques[0])
                subgraph = G_undirected.subgraph(first_n_clique)
                sub_adj_matrix = nx.to_pandas_adjacency(subgraph)

                output_path = f"/Users/lisadounia/projets_masterQ1/Web-Mining/graph/{n}_clique_adjacency_matrix{count}.xlsx"
                sub_adj_matrix.to_excel(output_path)
                print(f"Matrice d'adjacence de la première {n}-clique exportée vers : {output_path}")

# (c) n-Clans
print(f"\n========== Analyse des Clans ==============")
def is_n_clan(graph, nodes, n):
    subgraph = graph.subgraph(nodes)
    return nx.diameter(subgraph) <= n

for n in range(2,5):
    count = 0
    print(f"\n=== Analyse des {n}-clans ===")
    n_clans = [list(clique) for clique in n_cliques if is_n_clan(G_undirected, clique, n)]
    print(f"Nombre de {n}-clans : {len(n_clans)}")


    for i, clan in enumerate(n_clans, 1):
        print(f"{n}-clan {i} : {len(clan)}")
        if len(clan)>0:
            count+=1
            # Exporter la première n-clan en matrice d'adjacence
            first_n_clan = n_clans[0]
            subgraph = G_undirected.subgraph(first_n_clan)
            sub_adj_matrix = nx.to_pandas_adjacency(subgraph)

            output_path = f"/Users/lisadounia/projets_masterQ1/Web-Mining/graph/{n}_clan_adjacency_matrix{count}.xlsx"
            sub_adj_matrix.to_excel(output_path)
            print(f"Matrice d'adjacence de la première {n}-clan exportée vers : {output_path}")

# (d) k-Core
print(f"\n========== Analyse des k-Core ==============")
for k in range(2, 5):
    count=0
    print(f"\n=== Analyse du {k}-core ===")
    k_core = nx.k_core(G_undirected, k=k)
    print(f"Nombre de nœuds dans le {k}-core : {len(k_core.nodes())}")

    if len(k_core.nodes()) > 0:
        count+=1


        # Exporter la matrice d'adjacence du k-core
        k_core_adj_matrix = nx.to_pandas_adjacency(k_core)
        output_path = f"/Users/lisadounia/projets_masterQ1/Web-Mining/graph/{k}_core_adjacency_matrix{count}.xlsx"
        k_core_adj_matrix.to_excel(output_path)
        print(f"Matrice d'adjacence du {k}-core exportée vers : {output_path}")
