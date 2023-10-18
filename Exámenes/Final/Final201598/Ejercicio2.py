class MatDispDicc:
    # =================================================================
    # 2.1)
    # =================================================================
    def __init__(self, m, n, default=0, tipo='ren-col'):
        if tipo != "ren-col" and tipo != "col-ren" and tipo != "ambos":
            raise ValueError("Tipo inválido.")
        self.m = m
        self.n = n
        self.default = default
        self.tipo = tipo
        self.valoresRenCol = {}
        self.valoresColRen = {}
        self.max_len = 2
        self.colisiones = 0


    # =================================================================
    # 2.2)
    # =================================================================

    # Guarda datos en la matriz
    def guarda(self, i, j, valor, tipo=None):

        # Verificamos casos con tipos no debidos
        if self.tipo != "ambos" and tipo: raise ValueError("No se debe indicar tipo, pues el de esta matriz está ya determinado.")
        if self.tipo == "ambos" and tipo != "ren-col" and tipo != "col-ren": raise ValueError("Tipo especificado inválido.")

        # Si ya está determinado el tipo de matriz, guardamos ese valor en tipo
        if not tipo:
            tipo = self.tipo

        # Eliminamos lo que pudiera haber, si había algo, contamos la colisión
        if self.valoresRenCol.get((i,j), None) or self.valoresColRen.get((j,i), None):
            self.colisiones += 1

        # Almacenamos
        if tipo == "ren-col":
            self.valoresRenCol[(i, j)] = valor
        else:
            self.valoresColRen[(j, i)] = valor

        # Actualizamos máxima longitud de número (útil para la impresión)
        if len(str(valor)) > self.max_len:
            self.max_len = len(str(valor))
        
    # Recupera datos de la matriz
    def recupera(self, i, j):
        # Buscamos en ambos formatos. No nos importa el tipo, si no es el propio, ese dict estará vacío
        if (i,j) in self.valoresRenCol:
            return self.valoresRenCol[(i,j)]
        if (j, i) in self.valoresColRen:
            return self.valoresColRen[(j, i)]
        return self.default


    # =================================================================
    # 2.3.1)
    # =================================================================
    
    # Operación de transposición
    def transpuesta(self):
        nuevaMat = MatDispDicc(self.n, self.m, self.default, self.tipo)
        nuevaMat.valoresRenCol = {(j, i): v for (i, j), v in self.valoresRenCol.items()} # Intercambiamos renglones por columnas
        nuevaMat.valoresColRen = {(i, j): v for (j, i), v in self.valoresColRen.items()} # Intercambiamos columnas por renglones
        nuevaMat.max_len = self.max_len
        # Nota. Podríamos intercambias los diccionarios, pero habría varios subcasos. Por fines de simplicidad, se itera de esta manera
        return nuevaMat
    

    # =================================================================
    # 2.3.2)
    # =================================================================

    # Impresión por renglón
    def impRen(self, i):

        # Iteramos sobre columnas
        print(f'{i:{self.max_len-1}}'+"|", end=' ')
        for j in range(self.n):
            print(f'{self.recupera(i, j):{self.max_len}}', end=' ')    # Longitud estandarizada

    # Impresión por columna
    def impCol(self, j):
        # Iteramos sobre renglones
        print("\u0332".join(f'{j:{self.max_len}}'))
        for i in range(self.n):
            print(f'{self.recupera(i, j):{self.max_len}}', end='\n')    # Longitud estandarizada

    # Impresión total
    def impMat(self):
        # Iteramos sobre renglones
        print("\u0332".join(f'{"i|":{self.max_len}}'), end=' ')
        for k in [f'{i:{self.max_len}}' for i in range(self.n)]: print("\u0332".join(k), end=' ')
        print()
        for i in range(self.m):
            self.impRen(i)     # Imprimimos cada renglón
            print()


    # =================================================================
    # 2.3.3)
    # =================================================================
    
    # Suma de matrices del tipo self + otra
    def suma(self, otra):

        # Checamos dimensiones
        if self.m != otra.m or self.n != otra.n:
            raise ValueError('Las matrices deben tener las mismas dimensiones para la suma.')
        
        # Creamos matriz donde almacenaremos la suma y copiamos datos de esta
        res = MatDispDicc(self.m, self.n, self.default, self.tipo)
        res.max_len = self.max_len
        res.valoresRenCol = self.valoresRenCol.copy()
        res.valoresColRen = self.valoresColRen.copy()

        # Actualizamos tipo de la nueva
        if res.tipo == "ambos" or otra.tipo == "ambos" or res.tipo != otra.tipo:
            res.tipo = "ambos"

        # Iteramos sobre los datos guardados por ren-col de la otra matriz
        for (i, j), v in otra.valoresRenCol.items():
            # Aquí no nos sirve el método busca, pues no nos indica en qué dict está almacenada
            if (i, j) in res.valoresRenCol:    
                res.valoresRenCol[(i, j)] += v  # Si está en los valores ren-col de la original, lo sumamos
            elif (j, i) in res.valoresColRen:
                res.valoresColRen[(j, i)] += v  # Si está en los valores col-ren de la original, lo sumamos
            else:
                res.valoresRenCol[(i, j)] = v   # Si no está, lo ponemos en los ren-col de la nueva

        # Iteramos sobre los datos guardados por col-ren de la otra matriz
        for (j, i), v in otra.valoresColRen.items():
            if (i, j) in res.valoresRenCol:
                res.valoresRenCol[(i, j)] += v  # Repetimos
            elif (j, i) in res.valoresColRen:
                res.valoresColRen[(j, i)] += v  # Repetimos
            else:
                res.valoresColRen[(j, i)] = v   # Si no está, lo ponemos en los col-ren de la nueva

        return res
    

    # =================================================================
    # 2.3.4)
    # =================================================================

    # Multiplicación del tipo self * otra
    def multiplica(self, otra):

        # Verificamos dimensiones
        if self.n != otra.m:
            raise ValueError('El número de col-rens de la primera matriz debe ser igual al número de filas de la segunda para la multiplicación.')
        
        # Creamos matriz donde almacenaremos la multiplicación
        res = MatDispDicc(self.m, self.n, self.default, self.tipo)
        res.max_len = self.max_len

        # Actualizamos tipo de la nueva
        if res.tipo == "ambos" or otra.tipo == "ambos" or res.tipo != otra.tipo:
            res.tipo = "ambos"

        # Iteramos sobre los valores almacenados por ren-col
        for (i, k), v in self.valoresRenCol.items():
            # Iteramos sobre columnas para multiplicar
            for j in range(otra.n):
                v_otra = otra.recupera(k, j)
                # Buscamos aquel que tenga algún valor
                if v_otra != otra.default:
                    key = (i, j)
                    val = v*v_otra
                    if key in res.valoresRenCol:
                        res.valoresRenCol[key] += val
                        val = res.valoresRenCol[key] # Lo guardamos para actualizar la len
                    else:
                        res.valoresRenCol[key] = val

                    # Actualizamos la len
                    if res.max_len < len(str(val)):
                        res.max_len = len(str(val))
        
        # Iteramos sobre los valores almacenados por col-ren
        for (k, i), v in self.valoresColRen.items():
            # Iteramos sobre columnas para multiplicar
            for j in range(otra.n):
                v_otra = otra.recupera(k, j)
                # Buscamos aquel que tenga algún valor
                if v_otra != otra.default:
                    key = (i, j)
                    val = v*v_otra
                    if key in res.valoresRenCol:
                        res.valoresRenCol[key] += val
                        val = res.valoresRenCol[key] # Lo guardamos para actualizar la len
                    elif key in res.valoresColRen:      # Se agrega este caso a diferencia del ciclo ren-col, pues ahí era imposible que existiera
                        res.valoresColRen[key] += val
                        val = res.valoresRenCol[key] # Lo guardamos para actualizar la len
                    else:
                        res.valoresColRen[key] = val

                    # Actualizamos la len
                    if res.max_len < len(str(val)):
                        res.max_len = len(str(val))
        return res
    
# =================================================================
# 2.4)
# =================================================================
import random, time

# Con esto probamos la inserción
def generaMatDispersa(m, n, density, default=0, tipo='ren-col', imprim=False):
    mat = MatDispDicc(m, n, default, tipo)
    for k in range(int(m * n * density)):
        i = random.randint(0, m - 1)
        j = random.randint(0, n - 1)
        valor = random.randint(1, 10)
        if imprim: print("Insertando ", valor, " en ", str((i,j)))
        mat.guarda(i, j, valor)
    if imprim: print()
    return mat
    
# Prueba de programa
def evaluaMatDispDicc(M1, N1, default1, M2, N2, default2, sem, d1, d2, imprim=False):
    t0 = time.time()
    random.seed(sem)

    if imprim: print("Mat 1")
    mat1 = generaMatDispersa(M1, N1, d1, default=default1, imprim=imprim)
    if imprim: print("Mat 2")
    mat2 = generaMatDispersa(M2, N2, d2, tipo="col-ren", default=default2, imprim=imprim)

    # Imprimimos las matrices generadas
    if imprim:
        print("Matriz 1:")
        mat1.impMat()
        print("\nMatriz 2:")
        mat2.impMat()

    # Prueba del método de recuperación
    elems = [(random.randint(0, M1-1), random.randint(0, N1 - 1)) for i in range(int(M1*N1*0.25))]
    for (i, j) in elems:
        val = mat1.recupera(i, j)
        if imprim: print("Recuperamos el elemento ("+str(i)+", "+str(j)+") de la Matriz 1: ", val)

    # Prueba del método de transposición
    mat2_transpuesta = mat2.transpuesta()
    if imprim:
        print(f"\nTranspuesta de la Matriz 2:")
        mat2_transpuesta.impMat()

    # Prueba de los métodos de suma y multiplicación
    matriz_suma = mat1.suma(mat2)
    if imprim:
        print("\nSuma de las matrices 1 y 2:")
        matriz_suma.impMat()

    matriz_producto = mat1.multiplica(mat2)
    if imprim:
        print("\nProducto de mat 1 * mat 2:")
        matriz_producto.impMat()

    if imprim:
        renglon, columna = 6, 5
        print(f"\nImpresión del renglón {renglon} de la Matriz 1:")
        mat1.impRen(renglon)
        print()
        print(f"\nImpresión de la columna {columna} de la Matriz 1:")
        mat1.impCol(columna)

        # Conteo de colisiones
        print("\n Num de colisiones en mat 1: ", mat1.colisiones)
    t1 = time.time()
    return t1-t0

# Establecemos los parámetros para las matrices dispersas
sem = 1001
M1, N1 = 10, 10
M2, N2 = 10, 10
d1, d2 = 0.75, 0.75

# Llamamos el probador
evaluaMatDispDicc(M1, N1, 0, M2, N2, 0, sem, d1, d2, imprim=True)
    
# =================================================================
# Impresión de esta parte
# =================================================================

"""
Mat 1
Insertando  2  en  (0, 3)
Insertando  3  en  (8, 6)
Insertando  10  en  (6, 5)
Insertando  4  en  (6, 9)
Insertando  1  en  (9, 0)
Insertando  4  en  (7, 9)
Insertando  3  en  (8, 9)
Insertando  2  en  (0, 9)
Insertando  2  en  (6, 2)
Insertando  10  en  (4, 6)
Insertando  9  en  (1, 8)
Insertando  5  en  (6, 1)
Insertando  7  en  (5, 2)
Insertando  2  en  (0, 2)
Insertando  1  en  (9, 3)
Insertando  6  en  (6, 9)
Insertando  9  en  (3, 2)
Insertando  10  en  (7, 3)
Insertando  6  en  (0, 0)
Insertando  2  en  (6, 2)
Insertando  4  en  (5, 8)
Insertando  2  en  (0, 9)
Insertando  10  en  (3, 8)
Insertando  1  en  (5, 7)
Insertando  3  en  (7, 0)
Insertando  8  en  (2, 1)
Insertando  2  en  (4, 4)
Insertando  2  en  (0, 3)
Insertando  9  en  (7, 3)
Insertando  2  en  (8, 5)
Insertando  6  en  (1, 9)
Insertando  8  en  (8, 5)
Insertando  5  en  (0, 7)
Insertando  7  en  (5, 7)
Insertando  9  en  (4, 8)
Insertando  2  en  (5, 3)
Insertando  9  en  (4, 2)
Insertando  4  en  (2, 1)
Insertando  5  en  (4, 8)
Insertando  2  en  (1, 1)
Insertando  4  en  (1, 1)
Insertando  9  en  (1, 3)
Insertando  9  en  (7, 6)
Insertando  8  en  (9, 1)
Insertando  6  en  (0, 3)
Insertando  1  en  (8, 8)
Insertando  8  en  (1, 1)
Insertando  8  en  (3, 3)
Insertando  10  en  (2, 2)
Insertando  5  en  (1, 5)
Insertando  8  en  (9, 4)
Insertando  2  en  (1, 7)
Insertando  7  en  (4, 4)
Insertando  3  en  (7, 0)
Insertando  8  en  (6, 2)
Insertando  4  en  (8, 4)
Insertando  10  en  (1, 8)
Insertando  9  en  (5, 8)
Insertando  3  en  (7, 7)
Insertando  4  en  (8, 2)
Insertando  5  en  (8, 2)
Insertando  7  en  (0, 4)
Insertando  10  en  (0, 1)
Insertando  5  en  (8, 7)
Insertando  6  en  (9, 4)
Insertando  1  en  (1, 8)
Insertando  8  en  (4, 8)
Insertando  5  en  (2, 6)
Insertando  4  en  (9, 2)
Insertando  5  en  (0, 8)
Insertando  8  en  (6, 5)
Insertando  1  en  (1, 9)
Insertando  4  en  (9, 6)
Insertando  6  en  (6, 3)
Insertando  10  en  (7, 1)

Mat 2
Insertando  9  en  (3, 6)
Insertando  2  en  (9, 7)
Insertando  2  en  (0, 7)
Insertando  10  en  (7, 1)
Insertando  2  en  (2, 0)
Insertando  9  en  (5, 0)
Insertando  4  en  (2, 5)
Insertando  9  en  (9, 1)
Insertando  2  en  (4, 9)
Insertando  3  en  (0, 2)
Insertando  6  en  (1, 7)
Insertando  5  en  (2, 5)
Insertando  8  en  (9, 1)
Insertando  10  en  (8, 4)
Insertando  5  en  (6, 6)
Insertando  3  en  (3, 0)
Insertando  9  en  (7, 2)
Insertando  6  en  (1, 1)
Insertando  8  en  (8, 9)
Insertando  4  en  (8, 0)
Insertando  2  en  (1, 8)
Insertando  4  en  (5, 1)
Insertando  10  en  (9, 7)
Insertando  10  en  (9, 9)
Insertando  10  en  (0, 7)
Insertando  1  en  (5, 6)
Insertando  9  en  (3, 8)
Insertando  10  en  (3, 3)
Insertando  9  en  (7, 1)
Insertando  3  en  (4, 7)
Insertando  3  en  (8, 4)
Insertando  9  en  (1, 6)
Insertando  3  en  (9, 4)
Insertando  5  en  (5, 4)
Insertando  5  en  (0, 2)
Insertando  1  en  (7, 8)
Insertando  2  en  (1, 6)
Insertando  8  en  (3, 9)
Insertando  2  en  (7, 1)
Insertando  10  en  (2, 0)
Insertando  8  en  (7, 6)
Insertando  8  en  (8, 3)
Insertando  10  en  (6, 0)
Insertando  8  en  (6, 6)
Insertando  8  en  (6, 8)
Insertando  7  en  (4, 3)
Insertando  9  en  (8, 0)
Insertando  10  en  (7, 7)
Insertando  9  en  (5, 4)
Insertando  3  en  (0, 9)
Insertando  3  en  (3, 1)
Insertando  5  en  (3, 8)
Insertando  9  en  (0, 7)
Insertando  9  en  (2, 7)
Insertando  3  en  (5, 1)
Insertando  9  en  (6, 5)
Insertando  2  en  (9, 0)
Insertando  2  en  (1, 2)
Insertando  4  en  (4, 2)
Insertando  10  en  (0, 5)
Insertando  3  en  (4, 6)
Insertando  6  en  (1, 4)
Insertando  8  en  (0, 9)
Insertando  3  en  (0, 9)
Insertando  3  en  (7, 7)
Insertando  10  en  (7, 7)
Insertando  3  en  (7, 9)
Insertando  2  en  (8, 3)
Insertando  5  en  (3, 4)
Insertando  2  en  (6, 1)
Insertando  6  en  (3, 2)
Insertando  7  en  (4, 3)
Insertando  10  en  (1, 8)
Insertando  8  en  (8, 1)
Insertando  2  en  (2, 8)

Matriz 1:
i̲|  ̲0  ̲1  ̲2  ̲3  ̲4  ̲5  ̲6  ̲7  ̲8  ̲9
0|  6 10  2  6  7  0  0  5  5  2
1|  0  8  0  9  0  5  0  2  1  1
2|  0  4 10  0  0  0  5  0  0  0
3|  0  0  9  8  0  0  0  0 10  0
4|  0  0  9  0  7  0 10  0  8  0
5|  0  0  7  2  0  0  0  7  9  0
6|  0  5  8  6  0  8  0  0  0  6
7|  3 10  0  9  0  0  9  3  0  4
8|  0  0  5  0  4  8  3  5  1  3
9|  1  8  4  1  6  0  4  0  0  0

Matriz 2:
i̲|  ̲0  ̲1  ̲2  ̲3  ̲4  ̲5  ̲6  ̲7  ̲8  ̲9
0|  0  0  5  0  0 10  0  9  0  3
1|  0  6  2  0  6  0  2  6 10  0
2| 10  0  0  0  0  5  0  9  2  0
3|  3  3  6 10  5  0  9  0  5  8
4|  0  0  4  7  0  0  3  3  0  2
5|  9  3  0  0  9  0  1  0  0  0
6| 10  2  0  0  0  9  8  0  8  0
7|  0  2  9  0  0  0  8 10  1  3
8|  9  8  0  2  3  0  0  0  0  8
9|  2  8  0  0  3  0  0 10  0 10
Recuperamos el elemento (6, 5) de la Matriz 1:  8
Recuperamos el elemento (8, 0) de la Matriz 1:  0
Recuperamos el elemento (9, 7) de la Matriz 1:  0
Recuperamos el elemento (8, 2) de la Matriz 1:  5
Recuperamos el elemento (9, 0) de la Matriz 1:  1
Recuperamos el elemento (2, 7) de la Matriz 1:  0
Recuperamos el elemento (7, 7) de la Matriz 1:  3
Recuperamos el elemento (8, 6) de la Matriz 1:  3
Recuperamos el elemento (6, 8) de la Matriz 1:  0
Recuperamos el elemento (6, 1) de la Matriz 1:  5
Recuperamos el elemento (0, 2) de la Matriz 1:  2
Recuperamos el elemento (6, 4) de la Matriz 1:  0
Recuperamos el elemento (8, 1) de la Matriz 1:  0
Recuperamos el elemento (1, 8) de la Matriz 1:  1
Recuperamos el elemento (2, 8) de la Matriz 1:  0
Recuperamos el elemento (2, 7) de la Matriz 1:  0
Recuperamos el elemento (5, 7) de la Matriz 1:  7
Recuperamos el elemento (4, 4) de la Matriz 1:  7
Recuperamos el elemento (1, 1) de la Matriz 1:  8
Recuperamos el elemento (2, 3) de la Matriz 1:  0
Recuperamos el elemento (8, 5) de la Matriz 1:  8
Recuperamos el elemento (3, 5) de la Matriz 1:  0
Recuperamos el elemento (5, 7) de la Matriz 1:  7
Recuperamos el elemento (1, 9) de la Matriz 1:  1
Recuperamos el elemento (2, 0) de la Matriz 1:  0

Transpuesta de la Matriz 2:
i̲|  ̲0  ̲1  ̲2  ̲3  ̲4  ̲5  ̲6  ̲7  ̲8  ̲9
0|  0  0 10  3  0  9 10  0  9  2
1|  0  6  0  3  0  3  2  2  8  8
2|  5  2  0  6  4  0  0  9  0  0
3|  0  0  0 10  7  0  0  0  2  0
4|  0  6  0  5  0  9  0  0  3  3
5| 10  0  5  0  0  0  9  0  0  0
6|  0  2  0  9  3  1  8  8  0  0
7|  9  6  9  0  3  0  0 10  0 10
8|  0 10  2  5  0  0  8  1  0  0
9|  3  0  0  8  2  0  0  3  8 10

Suma de las matrices 1 y 2:
i̲|  ̲0  ̲1  ̲2  ̲3  ̲4  ̲5  ̲6  ̲7  ̲8  ̲9
0|  6 10  7  6  7 10  0 14  5  5
1|  0 14  2  9  6  5  2  8 11  1
2| 10  4 10  0  0  5  5  9  2  0
3|  3  3 15 18  5  0  9  0 15  8
4|  0  0 13  7  7  0 13  3  8  2
5|  9  3  7  2  9  0  1  7  9  0
6| 10  7  8  6  0 17  8  0  8  6
7|  3 12  9  9  0  0 17 13  1  7
8|  9  8  5  2  7  8  3  5  1 11
9|  3 16  4  1  9  0  4 10  0 10

Producto de mat 1 * mat 2:
i̲|̲   ̲ ̲0  ̲ ̲1  ̲ ̲2  ̲ ̲3  ̲ ̲4  ̲ ̲5  ̲ ̲6  ̲ ̲7  ̲ ̲8  ̲ ̲9
 0|  87 144 159 119 111  70 135 223 139 155
 1|  83 110  88  92 144   0 118  78 127  96
 2| 150  34   8   0  24  95  48 114 100   0
 3| 204 104  48 100  70  45  72  81  58 144
 4| 262  84  28  65  24 135 101 102  98  78
 5| 157  92  75  38  37  35  74 133  31 109
 6| 182 120  46  60 150  40  72 162  96 108
 7| 125 143 116  90 117 111 197 157 220 130
 8| 167  72  61  30  84  52  84 137  39  61
 9|  83  59  51  52  53  66  75 111 125  23

Impresión del renglón 6 de la Matriz 1:
6|  0  5  8  6  0  8  0  0  0  6

Impresión de la columna 5 de la Matriz 1:
 ̲5
 0
 5
 0
 0
 0
 0
 8
 0
 8
 0

 Num de colisiones en mat 1:  23
"""


# =================================================================
# Evalua dispersas vs densas
# =================================================================
import numpy as np

def evaluaMatDensa(M1, N1, M2, N2, sem, imprim=False):
    t0 = time.time()
    random.seed(sem)

    mat1 = np.random.randint(1,10, size=(M1,N1))
    mat2 = np.random.randint(1,10, size=(M2,N2))

    # Imprimimos las matrices generadas
    if imprim:
        print("Matriz 1:")
        print(mat1)
        print("\nMatriz 2:")
        print(mat2)

    # Prueba del método de recuperación
    elems = [(random.randint(0, M1-1), random.randint(0, N1 - 1)) for i in range(int(M1*N1*0.25))]
    for (i, j) in elems:
        val = mat1[i,j]
        if imprim: print("Recuperamos el elemento ("+str(i)+", "+str(j)+") de la Matriz 1: ", val)

    # Prueba del método de transposición
    mat2_transpuesta = mat2.transpose()
    if imprim:
        print(f"\nTranspuesta de la Matriz 2:")
        print(mat2_transpuesta)

    # Prueba de los métodos de suma y multiplicación
    matriz_suma = mat1 + mat2
    if imprim:
        print("\nSuma de las matrices 1 y 2:")
        print(matriz_suma)

    matriz_producto = np.matmul(mat1, mat2)
    if imprim:
        print("\nProducto de mat 1 * mat 2:")
        print(matriz_producto)

    if imprim:
        renglon, columna = 6, 5
        print(f"\nImpresión del renglón {renglon} de la Matriz 1:")
        print(mat1[renglon, :])
        print()
        print(f"\nImpresión de la columna {columna} de la Matriz 1:")
        print(mat2[:, columna])

    t1 = time.time()
    return t1-t0

print("="*60)
print("Comparación dispersa vs densa \n")
for n in range(50, 251, 50):
    print("Comparación para matriz "+str(n)+"x"+str(n)+": ")
    tiempoDisp = evaluaMatDispDicc(n, n, 0, n, n, 0, random.random(), 0.75, 0.75)
    tiempoDens = evaluaMatDensa(n, n, n, n, random.random())
    print("Tiempo de mat dispersa: ", tiempoDisp)
    print("Tiempo de mat densa: ", tiempoDens)
    print()
print("="*60)


"""
============================================================
Comparación dispersa vs densa

Comparación para matriz 50x50:
Tiempo de mat dispersa:  0.07524228096008301
Tiempo de mat densa:  0.0009965896606445312

Comparación para matriz 100x100:
Tiempo de mat dispersa:  0.43971848487854004
Tiempo de mat densa:  0.0059833526611328125

Comparación para matriz 150x150:
Tiempo de mat dispersa:  1.3296723365783691
Tiempo de mat densa:  0.03089737892150879

Comparación para matriz 200x200:
Tiempo de mat dispersa:  2.6843883991241455
Tiempo de mat densa:  0.03925752639770508

Comparación para matriz 250x250:
Tiempo de mat dispersa:  5.897439956665039
Tiempo de mat densa:  0.04687833786010742

============================================================
"""