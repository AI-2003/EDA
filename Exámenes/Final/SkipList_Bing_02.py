# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 13:40:53 2023

@author: RGAMBOAH
"""
# python
# Clase para representar un nodo de la skip list

import random

class Nodo:
    def __init__(self, valor, nivel):
        self.valor = valor # Valor almacenado en el nodo
        self.siguiente = [None] * (nivel + 1) # Lista de punteros al siguiente nodo en cada nivel
        
    def __str__(self):
       strRes = "Nodo:" + str(self.valor)
       return strRes

# Clase para representar una skip list
class SkipList:
    def __init__(self, max_level, p):
        self.max_level = max_level # Nivel máximo de la skip list
        self.p = p # Probabilidad de asignar un nivel aleatorio a un nuevo nodo
        self.cabeza = self.crear_nodo(None, max_level) # Nodo ficticio que actúa como cabeza de la lista
        self.nivel = 0 # Nivel actual de la lista

    # Función para crear un nuevo nodo con un valor y un nivel dados
    def crear_nodo(self, valor, nivel):
        return Nodo(valor, nivel)

    # Función para generar un nivel aleatorio para un nuevo nodo
    def nivel_aleatorio(self):
        import random
        nivel = 0
        while random.random() < self.p and nivel < self.max_level:
            nivel += 1
        return nivel

    # Función para insertar un nuevo elemento en la lista
    def insertar(self, valor):
        actual = self.cabeza # Nodo actual que recorre la lista
        actualizado = [None] * (self.max_level + 1) # Lista de nodos que deben ser actualizados después de la inserción

        # Buscar la posición adecuada para insertar el nuevo nodo
        for i in range(self.nivel, -1, -1):
            while actual.siguiente[i] and actual.siguiente[i].valor < valor:
                actual = actual.siguiente[i]
            actualizado[i] = actual # Guardar el nodo anterior al nuevo nodo en cada nivel

        actual = actual.siguiente[0] # Moverse al siguiente nodo del nivel más bajo

        # Si el valor ya existe en la lista, no hacer nada
        if actual and actual.valor == valor:
            return

        # Si el valor no existe, crear un nuevo nodo con un nivel aleatorio
        nivel_nuevo = self.nivel_aleatorio()
        nuevo_nodo = self.crear_nodo(valor, nivel_nuevo)

        # Si el nivel del nuevo nodo es mayor que el nivel actual de la lista, actualizar el nivel de la lista y la lista de nodos actualizados
        if nivel_nuevo > self.nivel:
            for i in range(self.nivel + 1, nivel_nuevo + 1):
                actualizado[i] = self.cabeza
            self.nivel = nivel_nuevo

        # Conectar el nuevo nodo con los nodos anteriores y siguientes en cada nivel
        for i in range(nivel_nuevo + 1):
            nuevo_nodo.siguiente[i] = actualizado[i].siguiente[i]
            actualizado[i].siguiente[i] = nuevo_nodo

    # Función para buscar un elemento en la lista
    def buscar(self, valor):
        actual = self.cabeza # Nodo actual que recorre la lista

        # Buscar el elemento desde el nivel más alto al más bajo
        for i in range(self.nivel, -1, -1):
            while actual.siguiente[i] and actual.siguiente[i].valor < valor:
                actual = actual.siguiente[i]

        # Moverse al siguiente nodo del nivel más bajo
        actual = actual.siguiente[0]

        # Si el elemento existe en la lista, devolverlo. Si no, devolver None.
        if actual and actual.valor == valor:
            return actual.valor
        else:
            return None

    # Elimina un valor
    def eliminar(self, valor):
        actual = self.cabeza # Nodo actual que recorre la lista
        actualizado = [None] * (self.max_level + 1) # Lista de nodos que deben ser actualizados después de la eliminación

        # Buscar la posición del nodo que se va a eliminar
        for i in range(self.nivel, -1, -1):
            while actual.siguiente[i] and actual.siguiente[i].valor < valor:
                actual = actual.siguiente[i]
            actualizado[i] = actual # Guardar el nodo anterior al nodo eliminado en cada nivel

        actual = actual.siguiente[0] # Moverse al siguiente nodo del nivel más bajo

        # Si el valor existe en la lista, eliminarlo
        if actual and actual.valor == valor:
            # Conectar los nodos anteriores y siguientes en cada nivel
            i == 0
            while i<=self.nivel and actualizado[i].siguiente[i] == actual:
                actualizado[i].siguiente[i] = actual.siguiente[i]
                i+=1

            # Reducir el nivel de la lista si el nodo eliminado era el único en su nivel
            while self.nivel > 0 and not self.cabeza.siguiente[self.nivel]:
                self.nivel -= 1

            return valor # El valor se encontró y se eliminó

        return None # El valor no se encontró



    def __str__(self):
        strRes = "Skip List: "
        nodo = self.cabeza
        while nodo != None:
            strRes += str(nodo) + "-->"
            nodo = nodo.siguiente[0]
        return strRes
    
    def imp(self):
        strRes = "Estructura de la skip List:\n"
        for nivel in range(self.max_level-1,-1,-1):
            strRes += "Nivel: " + str(nivel) + "\n"
            nodo = self.cabeza
            while nodo != None:
                strRes += str(nodo) + "-->"
                nodo = nodo.siguiente[nivel]
            strRes += "\n"
        return strRes    
        
"""
if __name__ == "__main__":
  
  max_level = 7
  p         = 0.5  
  SL = SkipList(max_level,p)
    
  for k in range(100):
      Key = int( 1000 * random.random())
      SL.insertar(Key)
      
  print(str(SL)) 
  print("="*60)
  print(SL.imp())
"""