import random
import numpy as np
import time
import copy

np.set_printoptions(linewidth=180, suppress = None, edgeitems=2000,threshold = 5000, formatter={'float': '{:4.0f}'.format})

cadsep           = "=" * 100
cadast           = "*" * 50
ALEATORIZA       = False
MATRIZ_SIMETRICA = True
SEMILLA          = 4967 #random.randint(1,10000)
TRAZA            = False

# =============================================================================
#                          gendist
# =============================================================================
def gendist(n, dmin,dmax,ftipo=np.ceil,dens = 0.5):
    #
    #   ftipo es np.ceil, np.floor, np.round
    #
    if not ALEATORIZA:
        random.seed(SEMILLA)
        print("SEMILLA=",SEMILLA)
    d = np.zeros((n,n))   
    deltaD = dmax - dmin
    for i in range(n):
          for j in range(n):
            if i == j:    
              d[i][j] = np.Inf
            else:    
              if random.random() < dens:
                  d[i][j] = int(ftipo(dmin + deltaD * random.random()))
                  #if random.random() < 0.25:
                  #    d[i][j] = -d[i][j]
              else:
                  d[i][j] = np.inf
                  
    return d        

# =============================================================================
#                         gendistSim
# =============================================================================
def gendistSim(n, dmin,dmax,ftipo=np.ceil,dens = 0.5):
    #
    
    #   ftipo es np.ceil, np.floor, np.round
    #
    if not ALEATORIZA:
        random.seed(SEMILLA)
        print("SEMILLA=",SEMILLA)
    d = np.zeros((n,n))   
    deltaD = dmax - dmin
    for i in range(n):
          for j in range(i+1):
              if random.random() < dens:
                  d[i][j] = int(ftipo(dmin + deltaD * random.random()))
              else:
                  d[i][j] = np.inf
    for i in range(n):
       d[i][i] = np.Inf 
       for j in range(i+1,n):
           d[i][j] = d[j][i]
    return d            
            
    
# =============================================================================

def distanciaMin(Matriz):
    n = len(Matriz)
    d_min = copy.deepcopy(Matriz)
    ut = copy.deepcopy(Matriz) # ultimo tramo
    for i in range(n):
        for j in range(n):
            if ut[i][j] < np.Inf:
                ut[i][j] = i
    for k in range(n):
        for i in range(n):
            if d_min[i][k] < np.Inf:
                for j in range(n):
                    d_ikj = d_min[i][k] + d_min[k][j]
                    if d_ikj < d_min[i][j]:
                        d_min[i][j] = d_ikj
                        ut[i][j] = k
                        
    return d_min,ut

def imprimeMatriz(strNombre, R):
    print("Matriz " + strNombre)
    n = len(R)
    for r in range(n):
        print(R[r])

def ruta(Ut, i, j):
    if Ut[i][j] == np.Inf:
        return []
    else:
        ruta=[j]
        pivote = int(Ut[i][j])
        ruta.append(pivote)
        while pivote != i:
            pivote = int(Ut[i][pivote])
            ruta.append(pivote)
        ruta = ruta[::-1]
        return ruta


def costo(D, ut, i, j):
    c = []
    r = ruta(ut, i, j)
    for k in range(1, len(r)):
        c.append([(r[k-1],r[k]),D[r[k-1]][r[k]]])
    return c



t0 = time.time()
n = 50
dmin = 1
dmax = 10
ftipo = np.ceil
dens = 0.5

Dist = gendist(n, dmin, dmax, ftipo, dens)

print(cadsep)
imprimeMatriz("Distancias", Dist)

print(cadsep)
Dist_min,Ut = distanciaMin(Dist)

imprimeMatriz("Distancias mínimas", Dist_min)
print(cadsep)
imprimeMatriz("UT", Ut)

print("Rutas entre nodos: ")
for i in range(n):
    for j in range(n):
        print(i, "->", j, ":", ruta(Ut,i,j), "costo:", costo(Dist_min, Ut, i, j))

t1 = time.time()
deltaT = t1-t0
print(cadsep)
print("n:",n,"DeltaT:",deltaT)
print(cadsep)




















