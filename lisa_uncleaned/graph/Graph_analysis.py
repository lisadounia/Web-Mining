import numpy as np
from numpy.linalg import norm
from numpy.linalg import inv
import math
import networkx as nx
from networkx import betweenness_centrality
A = np.array([[0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
[1, 0, 1, 1, 0, 0, 1, 0, 0, 0],
[1, 1, 0, 1, 1, 0, 1, 0, 0, 0],
[1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
[1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
[0, 0, 0, 0, 0, 1, 0, 1, 1, 0]],int)

### Pour les voisins communs
#print(np.dot(A,A))

Simcomment = np.zeros(A.shape)

for i in range(len(A)) : 
    for k in range(len(A)) : 
        for j in range(len(A)) : 
            Simcomment[i,k] += (A[i,j]*A[j,k])






#attachement préférentiel
# Calcul du degré de chaque nœud


Simcomment = np.zeros(A.shape)

for i in range(len(A)) : 
    for j in range(len(A)) :
        sommeligne = 0
        sommecolonne = 0
        for k in range(len(A)) : 
            sommeligne += A[i,k]
            sommecolonne += A[k,j]
        Simcomment[i,j] += sommeligne*sommecolonne

print(Simcomment)
######cosinus
Simcomment = np.zeros(A.shape)
for i in range(len(A)) : 
    for j in range(len(A)) :
        sommeligne = 0
        sommecolonne = 0
        prochevoisins = 0
        for k in range(len(A)) : 
            sommeligne += A[i,k]
            sommecolonne += A[k,j]
            prochevoisins += A[i,k]*A[k,j]
        Simcomment[i,j] += prochevoisins/(math.sqrt(sommeligne)*math.sqrt(sommecolonne))

print(Simcomment)
for i in range(len(Simcomment)) : 
    for j in range(len(Simcomment)) : 
        print(Simcomment[i,j],end="\t")
    print()


#DIICe 

Simcomment = np.zeros(A.shape)
for i in range(len(A)) : 
    for j in range(len(A)) :
        sommeligne = 0
        sommecolonne = 0
        prochevoisins = 0
        for k in range(len(A)) : 
            sommeligne += A[i,k]
            sommecolonne += A[k,j]
            prochevoisins += A[i,k]*A[k,j]
        Simcomment[i,j] += 2*prochevoisins/((sommeligne)+(sommecolonne))

###JACCARD

Simcomment = np.zeros(A.shape)
for i in range(len(A)) : 
    for j in range(len(A)) :
        sommeligne = 0
        sommecolonne = 0
        prochevoisins = 0
        for k in range(len(A)) : 
            sommeligne += A[i,k]
            sommecolonne += A[k,j]
            prochevoisins += A[i,k]*A[k,j]
        Simcomment[i,j] += prochevoisins/((sommeligne)+(sommecolonne)-prochevoisins )

print(Simcomment)



#kkaaaaatz
def Katz(matrice,alpha) : 
    I = np.identity(len(matrice))
    matricekatz = [[0 for o in range(len(matrice))] for p in range(len(matrice))]
    matrice = np.array(matrice)
    matrice = inv(I-(alpha*matrice)) - I
    return matrice

print(Katz(A,0.2))

### création de la matrice P
Simcomment = np.zeros(A.shape)

for i in range(len(A)) : 
    for j in range(len(A)) :
        sommeligne = 0
        sommecolonne = 0
        for k in range(len(A)) : 
            sommeligne += A[i,k]
        Simcomment[i,j] += A[i,j]/sommeligne
    
print(Simcomment)

### création matrice D

D = np.zeros(A.shape)

for i in range(len(A)) : 
    sommeligne = 0
    sommecolonne = 0
    for k in range(len(A)) : 
        sommeligne += A[i,k]
    D[i,i] += sommeligne

L = D-A

e = np.ones((len(D),1))
print(e)

result = np.dot(e, e.T) / len(D)

lplus = inv(L-result)+result
print(lplus)

def mki(lplus,D,i,k) : 
    mki = 0
    for j in range(len(lplus)) : 
        mki += (lplus[i,j]-lplus[i,k]-lplus[k,j]+lplus[k,k])*D[j,j]
    return mki

FPT = np.zeros(A.shape)
for i in range(len(A)) : 
    for K in range(len(A)) : 
        FPT[i,K] += mki(lplus,D,i,K)

print(FPT)


ct = FPT + FPT.T
print(ct)

def preprocess(mat):
    x = len(mat)
    y = len(mat[0])
    for i in range(x):
        for j in range(y):
            if mat[i, j] == 0:
                mat[i, j] = 100000
    return mat
def floyd(mat):
    x = len(mat)
    y = len(mat[0])
    SP = preprocess(mat)
    if x == y:
        for k in range(x):
            for i in range(x):
                for j in range(x):
                    SP[i,j]=min((SP[i,k]+SP[k,j],SP[i,j]))
    else:
        print('error')
    for i in range(x):
        SP[i,i]=0
    return SP

ASPATH = (floyd(A))
print(ASPATH)
########closenessss
def cc(matriceSPATH) : 
    liste = []
    for i in matriceSPATH : 
        sum = 0
        for j in i :
            sum += j
        print(sum)
        liste.append(float((len(i)-1)/sum)) 
    return liste
G = nx.from_numpy_array(A)
print(cc(ASPATH))

