import pandas as pd
import networkx as nx

adj_matrix = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/adjacency_matrix_V2.xlsx', index_col=0)


G = nx.from_pandas_adjacency(adj_matrix, create_using=nx.DiGraph)
G_undirected = G.to_undirected()

#informations sur le graph
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
density = nx.density(G)
print(f"Taille de la matrice d'adjacence : {adj_matrix.shape}")
print(f"Nombre de nœuds : {num_nodes}")
print(f"Nombre d'arêtes : {num_edges}")
print(f"Densité du graphe : {density:.4f}")


#### Analyse des points d'articulation ####


articulation_points = list(nx.articulation_points(G_undirected))

print("=== Points d'articulation ===")
print(f"Nombre total de points d'articulation : {len(articulation_points)}")

# évaluation de l'impact de chaque point d'articulation
impact_scores = []
for node in articulation_points:
    G_temp = G_undirected.copy()
    G_temp.remove_node(node)  # Supprimer le nœud
    components = list(nx.connected_components(G_temp))  # Trouver les composantes restantes
    largest_component_size = max(len(comp) for comp in components)  # Taille de la plus grande composante
    impact_scores.append((node, len(components), largest_component_size))

# Trier les points d'articulation par leur impact (nombre de composantes créées aprés leur suppression)
impact_scores = sorted(impact_scores, key=lambda x: (x[1], -x[2]), reverse=True)

# Top 5 points d'articulation
top_5_articulation = impact_scores[:5]
print("\nTop 5 points d'articulation qui séparent les plus grandes composantes :")
for node, num_components, largest_size in top_5_articulation:
    print(f"Nœud {node} - Nombre de composantes après suppression : {num_components}, Taille de la plus grande composante : {largest_size}")

#### Analyse des ponts ####

bridges = list(nx.bridges(G_undirected))
print(f"Nombre total de ponts : {len(bridges)}")

#  évaluation de l'impact de chaque pont
bridge_impact_scores = []
for u, v in bridges:
    G_temp = G_undirected.copy()
    G_temp.remove_edge(u, v)  # Supprimer le pont
    components = list(nx.connected_components(G_temp))  # Trouver les composantes restantes
    largest_component_size = max(len(comp) for comp in components)  # Taille de la plus grande composante

    # Si un des nœuds du pont est connecté à Social Inequality
    connected_to_social_inequality_u = nx.has_path(G_temp, u, 'https://en.wikipedia.org/wiki/Social_inequality')
    connected_to_social_inequality_v = nx.has_path(G_temp, v, 'https://en.wikipedia.org/wiki/Social_inequality')
    bridge_impact_scores.append(((u, v), len(components), largest_component_size, connected_to_social_inequality_u, connected_to_social_inequality_v))

# Trier les ponts par leur impact
bridge_impact_scores = sorted(bridge_impact_scores, key=lambda x: (x[1], -x[2]), reverse=True)

# Afficher les ponts qui causent le plus de composantes
print("\nPonts causant le plus de composantes après suppression :")
for bridge, num_components, largest_size, connected_u, connected_v in bridge_impact_scores:
    print(f"Pont {bridge} - Nombre de composantes après suppression : {num_components}, "
          f"Taille de la plus grande composante : {largest_size}, "
          f"U connecté à Social Inequality : {connected_u}, "
          f"V connecté à Social Inequality : {connected_v}")


#### Analyse des SCC ####

strongly_connected_components = list(nx.strongly_connected_components(G))
scc_sizes = [len(comp) for comp in strongly_connected_components]
sorted_scc = sorted(strongly_connected_components, key=len, reverse=True)
## il n'y a qu'un seul SCC
scc = sorted_scc[0]
scc_nodes = sorted_scc[0]  # Le plus grand SCC
SCC = G.subgraph(scc_nodes).copy()  # Créer un sous-graphe pour ce SCC

#Informations sur le SCC
print(f"Taille du SCC : {len(SCC.nodes)} nœuds")
print(f"Nombre d'arêtes : {len(SCC.edges)}")
density = nx.density(SCC)
print(f"Densité du SCC : {density:.4f}")
if len(SCC) > 1:
    avg_shortest_path_length = nx.average_shortest_path_length(SCC)
    print(f"Distance géodésique moyenne : {avg_shortest_path_length:.2f}")

# Vérifier si tous les nœuds du SCC sont des nœuds fils de Social Inequality
social_inequality_node = "https://en.wikipedia.org/wiki/Social_inequality"
# Obtenir les voisin directs de Social Inequality dans le SCC
successors = list(SCC.successors(social_inequality_node))
all_children = True
non_children_nodes = []

for node in SCC.nodes:
    if node != social_inequality_node and node not in successors:
        all_children = False
        non_children_nodes.append(node)

print(f"Tous les nœuds du SCC sont des nœuds fils de Social Inequality : {all_children}")
if not all_children:
    print(f"Nœuds non fils de Social Inequality : {non_children_nodes}")

