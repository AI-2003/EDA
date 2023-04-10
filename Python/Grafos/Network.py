# ========================================
#               Utilerías
# ========================================

import sys

cadsep = "=" * 60

def letrero(strLetrero):
    print(cadsep)
    print("          " + strLetrero)
    print(cadsep)

def salir(strLetrero):
    letrero(strLetrero)
    sys.exit()	




# ========================================
#          Estructura topológica
# ========================================

class EstructuraTopo:

    def __init__(self):
        self.colNodos = {}

    def agrega(self, strAnt, strSuc):

        nodoAnt = self.colNodos.get(strAnt)
        nodoSuc = self.colNodos.get(strSuc)

        if nodoAnt == None:
            nodoAnt = NodoTopo(strAnt)
            self.colNodos[strAnt] = nodoAnt
        if nodoSuc == None:
            nodoSuc = NodoTopo(strSuc)
            self.colNodos[strSuc] = nodoSuc

        nodoAnt.colSucesores.append(nodoSuc)
        nodoSuc.num_antecesores += 1
    
    def ordenaT(self):
        pass

    def __str__(self):
        strRes = "EstructuraTopo\n"
        if len(self.colNodos) == 0: 
            strRes += "Colección de nodos vacía\n"
        for nodo in self.colNodos.values():
            strRes += str(nodo) + "\n"
        return strRes




# ========================================
#             Nodo topológico
# ========================================

class NodoTopo:
    
    def __init__ (self, strId):
        self.id = strId
        self.num_antecesores = 0
        self.colSucesores = []

    def __str__ (self):
        strRes = "NodoTopo " + str(self.id) + "\n"
        strRes += "Num. antecesotres: "+str(self.num_antecesores)+"\n"
        if len(self.colSucesores) == 0:
            strRes += "Sin sucesores\n"
        for suc in self.colSucesores:
            strRes += str(suc.id)
        return strRes




# ========================================
#           Programa principal
# ========================================

