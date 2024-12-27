import numpy as np
from numpy.linalg import inv
import pandas as pd
import math
from scipy.sparse import csr_matrix, identity
from scipy.sparse.linalg import inv as sparse_inv
from scipy.sparse.csgraph import floyd_warshall
from scipy.linalg import eigh
import scipy.sparse as sp
import scipy.sparse.linalg as splinalg

# Charger la matrice d'adjacence
adj_matrix = pd.read_excel('/Users/lisadounia/projets_masterQ1/Web-Mining/graph/adjacency_matrix_V2.xlsx', index_col=0).values

# Fonction pour exporter une matrice en Excel
def export_matrix(matrix, filename):
    df = pd.DataFrame(matrix)
    output_path = f'/Users/lisadounia/projets_masterQ1/Web-Mining/graph/similarity/{filename}.xlsx'
    df.to_excel(output_path, index=False, header=False)
    print(f"Matrice exportée : {output_path}")

# ================================
# 1. Mesures locales de similarité
# ================================

# (a) Voisins communs
Sim_common = np.dot(adj_matrix, adj_matrix)
export_matrix(Sim_common, "similarity_common_neighbors")

# (b) Co-citation et co-référence
Sim_co_citation = np.dot(adj_matrix.T, adj_matrix)
Sim_co_reference = np.dot(adj_matrix, adj_matrix.T)
export_matrix(Sim_co_citation, "similarity_co_citation")
export_matrix(Sim_co_reference, "similarity_co_reference")

# (c) Attachement préférentiel
degree_row = np.sum(adj_matrix, axis=1)  # Somme des lignes (degré sortant)
degree_col = np.sum(adj_matrix, axis=0)  # Somme des colonnes (degré entrant)
Sim_pref_attachment = np.outer(degree_row, degree_col)  # Produit extérieur pour éviter les boucles
export_matrix(Sim_pref_attachment, "similarity_preferential_attachment")

# ================================
# 1. Coefficients de similarité (Cosine, Dice, Jaccard)
# ================================

sum_row = adj_matrix.sum(axis=1)
intersection = np.dot(adj_matrix, adj_matrix.T)
norm_row = np.sqrt(np.sum(adj_matrix**2, axis=1))
union = np.add.outer(sum_row, sum_row) - intersection

# Cosine similarity
Sim_cosine = np.divide(
    intersection,
    np.outer(norm_row, norm_row),
    out=np.zeros_like(intersection, dtype=float),  # Spécifiez explicitement dtype=float
    where=(np.outer(norm_row, norm_row) != 0))
export_matrix(Sim_cosine, "similarity_cosine")

# Jaccard similarity
Sim_jaccard = np.divide(
    intersection,
    union,
    out=np.zeros_like(intersection, dtype=float),
    where=(union != 0)
)
export_matrix(Sim_jaccard, "similarity_jaccard")

# Dice similarity
Sim_dice = np.divide(2 * intersection, np.add.outer(sum_row, sum_row), out=np.zeros_like(intersection,dtype=float), where=(np.add.outer(sum_row, sum_row) != 0))
export_matrix(Sim_dice, "similarity_dice")


# ================================
# 2. Mesures globales de similarité
# ================================

# (a) Katz Similarity
def Katz(matrix, alpha):
    I = np.eye(len(matrix))
    try:
        # Ajout d'une régularisation pour éviter les matrices singulières
        katz_matrix = inv(I - alpha * matrix + np.eye(len(matrix)) * 1e-6) - I
        return katz_matrix
    except np.linalg.LinAlgError:
        print("Erreur : Matrice singulière lors du calcul de Katz.")
        return np.zeros_like(matrix)

Sim_katz = Katz(adj_matrix, alpha=0.2)
export_matrix(Sim_katz, "similarity_katz")

# (b) Random Walk Transition Matrix

row_sums = adj_matrix.sum(axis=1)
Sim_transition = np.divide(
    adj_matrix,
    row_sums[:, None],  # Broadcasting
    out=np.zeros_like(adj_matrix, dtype=float),  # Assurez-vous que le type est float
    where=(row_sums[:, None] != 0)
)
export_matrix(Sim_transition, "random_walk_transition_matrix")


# ================================
# 3. Modèles de diffusion et distances basées sur chemins
# ================================

def calculate_fpt_cm_sparse(adj_matrix):
    # Conversion en matrice creuse
    adj_sparse = sp.csr_matrix(adj_matrix)

    # Calcul de la matrice des degrés (creuse)
    degrees = np.array(adj_sparse.sum(axis=1)).flatten()
    D_sparse = sp.diags(degrees)

    # Matrice Laplacienne
    L_sparse = D_sparse - adj_sparse

    # Ajout de régularisation pour éviter les singularités
    n = adj_sparse.shape[0]
    eeT_sparse = sp.csr_matrix(np.ones((n, n)) / n)
    L_reg = L_sparse + sp.eye(n) * 1e-6 - eeT_sparse

    # Pseudo-inverse de la Laplacienne
    L_plus_sparse = sp.linalg.inv(L_reg).toarray()

    # Calcul de FPT
    FPT = np.zeros((n, n))
    for i in range(n):
        for k in range(n):
            if i != k:
                FPT[i, k] = np.sum(
                    (L_plus_sparse[i, :] - L_plus_sparse[i, k] - L_plus_sparse[k, :] + L_plus_sparse[k, k]) * degrees
                )

    # Calcul de CM
    CM = FPT + FPT.T
    return FPT, CM


# Calculer FPT et ACT
FPT, ACT = calculate_fpt_cm_sparse(adj_matrix)


export_matrix(FPT, "average_first_passage_time")
export_matrix(ACT, "average_commute_time")

# ================================
# 4. Centralités
# ================================

def closeness_centrality(sp_matrix):
    centrality = []
    for row in sp_matrix:
        total_distance = np.sum(row)
        if total_distance > 0:
            centrality.append((len(row) - 1) / total_distance)
        else:
            centrality.append(0)
    return centrality

Closeness = closeness_centrality(Shortest_path)
export_matrix(np.array(Closeness).reshape(-1, 1), "closeness_centrality")
