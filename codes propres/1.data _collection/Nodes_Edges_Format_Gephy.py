import pandas as pd
adjacency_matrix = pd.read_excel("/Users/lisadounia/projets_masterQ1/Web-Mining/adjacency_matrix_V2.xlsx", index_col=0)


nodes = pd.DataFrame({
    "Id": range(len(adjacency_matrix)),
    "Label": adjacency_matrix.index
})
nodes.to_excel("nodes.xlsx", index=False)

edges = []
for i, source in enumerate(adjacency_matrix.index):
    for j, target in enumerate(adjacency_matrix.columns):
        weight = adjacency_matrix.iloc[i, j]
        if weight > 0:  # Inclure uniquement les connexions existantes
            edges.append({"Source": source, "Target": target, "Weight": weight})

edges_df = pd.DataFrame(edges)
edges_df.to_excel("edges.xlsx", index=False)

