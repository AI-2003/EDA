# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 11:42:15 2023

@author: Armando Ibarrarán
"""
import time



def permuta(perm, disp, n, sig,c):
    if sig>n:
        if valida(perm, n):
            c[0]+=1
            print(c[0], perm[1:n+1])
        return
    for k in range(1, n+1):
            if disp[k]:
                perm[sig] = k
                disp[k] = False
                permuta(perm, disp, n, sig+1, c)
                disp[k] = True



# =============================================

def valida(p, n):
    valid = True
    i=1
    while valid and i<n:
        j = i+1
        while valid and j<=n:
            valid = abs(j-i) != abs(p[i]-p[j])
            j+=1
        i+=1
    return valid



# =============================================

cadsep = "="*60
 
print(cadsep)
n = 8
p = [0]*(n+1)
d = [True]*(n+1)


t0 = time.time()
permuta(p, d, n, 1, [0])
t1 = time.time()


print("DeltaT: ", t1-t0, "seg")

"""
print(p)
print(d)
"""
print("")

# =============================================

class Persona():
    def __init__(self, nombre, apellido, edad):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
    
    def __str__ (self):
        # Es obligatorio escribir las variables con self.
        res = "Persona: "+self.nombre+" "+self.apellido+" de "+str(self.edad)+" años"
        return res


per = Persona("Juan", "Camaney", 49)
print(str(per))




