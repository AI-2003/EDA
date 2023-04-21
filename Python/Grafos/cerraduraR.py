

import time
import random
import copy

ALEATORIZA = True

cadsep = "="*60



# ==============================
# Utilería
# ==============================

def relacion(n,d):
    R = []
    for k in range(n):
        R.append([0]*n)
    for i in range(n):
        for j in range(n):
            if random.random() <=d:
                R[i][j] = 1
    return R

def warshall(R):
    n = len(R)
    for k in range(n):
        for i in range(n):
            if R[i][k] == 1:
                for j in range(n):
                    if R[k][j] == 1:
                        R[i][j] == 1
    return R


def genMatBin(m, n):
    C = []
    for i in range(m):
        C.append([0]*n)
    return C

def multMatBin(A, B):
    ma = len(A)
    na = len(A[0])
    mb = len(B)
    nb = len(B[0])

    if na!=mb:
        return None
    
    C = genMatBin(ma, nb)

    for i in range(ma):
        for j in range(nb):
            for k in range(na):
                if A[i][k]*B[k][j] > 0:
                    C[i][j] = 1 
                    break   #### break!!!!
    return C

def sumMatBin(A,B):
    ma = len(A)
    na = len(A[0])
    mb = len(B)
    nb = len(B[0])

    if ma!=mb or na!=nb:
        return None
    
    C = genMatBin(ma, na)

    for i in range(ma):
        for j in range(na):
            C[i][j] = A[i][j] or B[i][j]

def matCerr(R):
    res = copy.deepcopy(R)
    n = len(R)

    for i in range(n-1):
        res = sumMatBin(res, res*R)
    return res



def impMatR(strNombre, R):
    print("Matriz "+ strNombre)
    n = len(R)
    for r in R:
        print(r)



# ==============================
# Programa principal
# ==============================

ALEATORIZA = True
SEMILLA = 1234

if ALEATORIZA:
    SEMILLA = int(random.random()*10000)
random.seed(SEMILLA)

print(cadsep)
print("SEMILLA: ", SEMILLA)

n = 10
dens = 0.1

R = relacion(n, dens)
print(cadsep)
impMatR("R", R)

Rpos = copy.deepcopy(R)
Rpos = warshall(Rpos)
print(cadsep)
impMatR("Rpos", Rpos)

print(cadsep)
print("SEMILLA: ", SEMILLA)

print(cadsep)

C = sumMatBin(R, Rpos)
print(C)
impMatR("Sum", C)
