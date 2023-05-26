class MatDisp:

    def __init__(self, m, n, default=0, tipo='ren-col'):
        self.m = m
        self.n = n
        self.default = default
        self.tipo = tipo
        self.valores = {}  # Diccionario para almacenar valores no predeterminados

    def insert(self, i, j, value):
        if self.tipo == 'ren-col':
            key = (i, j)
        elif self.tipo == 'col-ren':
            key = (j, i)
        self.valores[key] = value

    def get(self, i, j):
        if self.tipo == 'ren-col':
            key = (i, j)
        elif self.tipo == 'col-ren':
            key = (j, i)
        return self.valores.get(key, self.default)

    def transpuesta(self):
        t_mat = MatDisp(self.n, self.m, self.default, self.tipo)
        t_mat.valores = {(j, i): v for (i, j), v in self.valores.items()}
        return t_mat

    def imp(self):
        max_length = max(len(str(value)) for value in self.valores.valores()) # Encontramos el número con impresión más larga
        for i in range(self.m):
            for j in range(self.n):
                print(f'{self.get(i, j):{max_length}}', end=' ') # Todas las casillas quedan con la longitud del número más largo
            print()


    def suma(self, otra):
        if self.m != otra.m or self.n != otra.n:
            raise ValueError('Las matrices deben tener las mismas dimensiones para la suma.')
        res = MatDisp(self.m, self.n, self.default, self.tipo)
        res.valores = self.valores.copy()
        for (i, j), v in otra.valores.items():
            if (i, j) in res.valores:
                res.valores[(i, j)] += v
            else:
                res.valores[(i, j)] = v
        return res

    # Multiplicación self * otra
    def multiplica(self, otra):
        if self.n != otra.m:
            raise ValueError('El número de col-rens de la primera matriz debe ser igual al número de filas de la segunda para la multiplicación.')
        res = MatDisp(self.m, otra.n, self.default_value, self.method)
        for (i, k), v in self.values.items():
            for j in range(otra.n):
                if otra.get(k, j) != self.default_value:
                    key = (i, j)
                    if key in res.values:
                        res.values[key] += v * otra.get(k, j)
                    else:
                        res.values[key] = v * otra.get(k, j)
        return res



# ====================================
# Prueba
# ====================================

import random

def generaMatDispersa(m, n, density, default=0, tipo='ren-col'):
    mat = MatDisp(m, n, default, tipo)
    for k in range(int(m * n * density)):
        i = random.randint(0, m - 1)
        j = random.randint(0, n - 1)
        value = random.randint(1, 10)
        mat.insert(i, j, value)
    return mat

sem = 1001
random.seed(sem)  # Establece la semilla para la reproducibilidad

M1, N1 = 10, 10
M2, N2 = 10, 10
d1, d2 = 0.075, 0.075

mat1 = generaMatDispersa(M1, N1, d1)
mat2 = generaMatDispersa(M2, N2, d2)

# Prueba las operaciones
print("Matriz 1:")
mat1.imp()
print("\nMatriz 2:")
mat2.imp()

print("\nTransposición de la matriz 1:")
mat1.transpuesta().imp()

print("\nSuma de las matrices:")
mat1.suma(mat2).imp()
mat2.suma(mat1).imp()

print("\nMultiplicación de las matrices:")
mat1.multiply(mat2).imp()
