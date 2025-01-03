import pandas as pd
import networkx as nx
from collections import Counter
from networkx.algorithms.community import k_clique_communities

# Charger la matrice d'adjacence
adj_matrix = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/adjacency_matrix_V2.xlsx', index_col=0)
print(f"Taille de la matrice d'adjacence : {adj_matrix.shape}")

# Créer un graphe dirigé
G = nx.from_pandas_adjacency(adj_matrix, create_using=nx.DiGraph)

# Convertir en graphe non orienté
G_undirected = G.to_undirected()

# # ================================
# # 1. Informations générales
# # ================================
# print(f"Nombre de nœuds : {len(G.nodes)}")
# print(f"Nombre d'arêtes : {len(G.edges)}")
# density = nx.density(G)
# print(f"Densité du graphe : {density:.4f}")
#
# # Calculer le diamètre
# diameter = nx.diameter(G_undirected)
# print(f"Diamètre du graphe : {diameter}")
#
# # Distance géodésique moyenne
# if len(G_undirected) > 1:
#     avg_shortest_path_length = nx.average_shortest_path_length(G_undirected)
#     print(f"Distance géodésique moyenne : {avg_shortest_path_length:.2f}")

# ================================
# 2. Sous-groupes
# ================================

#
# print(f"\n========== Analyse des cliques ==============")
# cliques = list(nx.find_cliques(G_undirected))  # Trouver toutes les cliques maximales
# largest_clique = max(cliques, key=len)
# sorted_cliques = sorted(cliques, key=len, reverse=True)  # Trier par taille décroissante
#
# # Compter le nombre de cliques par taille
# clique_sizes = [len(clique) for clique in cliques]
# clique_count_by_size = Counter(clique_sizes)
#
# # Afficher le nombre total de cliques
# print(f"Nombre total de cliques : {len(cliques)}")
#
# # Afficher le nombre de cliques par taille
# print("\nNombre de cliques par taille :")
# for size, count in sorted(clique_count_by_size.items(), reverse=True):
#     print(f"- {count} cliques de taille {size}")
#
# # Afficher les 3 plus grandes cliques avec leurs nœuds
# print("\nTop 3 des plus grandes cliques :")
# for i, clique in enumerate(sorted_cliques[:3], 1):  # Les 3 plus grandes cliques
#     print(f"Clique {i} ({len(clique)} nœuds) : {clique}")
#



# # (b) n-Cliques
for n in range(5, 6):
    count=0
    print(f"\n=== Analyse des {n}-cliques ===")
    n_cliques = list(k_clique_communities(G_undirected, k=n))
#     print(f"Nombre de communautés {n}-cliques : {len(n_cliques)}")
#
#     if n_cliques:
#         for i, n_clique in enumerate(n_cliques, 1):
#             print(f"{n}-clique {i} ({len(n_clique)} nœuds)")
#             if len(n_clique)>0:
#                 count+=1
#                 # Exporter la première n-clique en matrice d'adjacence
#                 first_n_clique = list(n_cliques[0])
#                 subgraph = G_undirected.subgraph(first_n_clique)
#                 sub_adj_matrix = nx.to_pandas_adjacency(subgraph)
#
#                 output_path = f"/Users/lisadounia/projets_masterQ1/Web-Mining/graph/subgraph_cohesions/{n}_clique_adjacency_matrix{count}.xlsx"
#                 sub_adj_matrix.to_excel(output_path)
#                 print(f"Matrice d'adjacence de la première {n}-clique exportée vers : {output_path}")


def is_n_clan(graph, nodes, n):
    subgraph = graph.subgraph(nodes)
    if nx.is_connected(subgraph):  # Assurez-vous que le sous-graphe est connexe
        return nx.diameter(subgraph) <= n
    return False

print("\n========== Analyse des n-Clans (2 à 6) ==============")

# Parcourir les valeurs de n pour les n-clans
for n in range(2, 7):
    print(f"\n=== Analyse des {n}-clans ===")
    n_clans = []
    for clique in nx.find_cliques(G_undirected):  # Cliques maximales
        if len(clique) >= 5 and is_n_clan(G_undirected, clique, n):  # Exclure les clans avec moins de 10 nœuds
            n_clans.append(clique)

    # Afficher le nombre de n-clans trouvés
    print(f"Nombre de {n}-clans : {len(n_clans)}")

    # Afficher le nombre de nœuds dans chaque sous-graphe
    for i, clan in enumerate(n_clans, 1):
        print(f"{n}-clan {i} : {len(clan)} nœuds")

# # (d) k-Core
# print(f"\n========== Analyse des k-Core ==============")
# for k in range(2, 5):
#     count=0
#     print(f"\n=== Analyse du {k}-core ===")
#     k_core = nx.k_core(G_undirected, k=k)
#     print(f"Nombre de nœuds dans le {k}-core : {len(k_core.nodes())}")
#
#     if len(k_core.nodes()) > 0:
#         count+=1
#
#
#         # Exporter la matrice d'adjacence du k-core
#         k_core_adj_matrix = nx.to_pandas_adjacency(k_core)
#         output_path = f"/Users/lisadounia/projets_masterQ1/Web-Mining/graph/{k}_core_adjacency_matrix{count}.xlsx"
#         k_core_adj_matrix.to_excel(output_path)
#         print(f"Matrice d'adjacence du {k}-core exportée vers : {output_path}")
