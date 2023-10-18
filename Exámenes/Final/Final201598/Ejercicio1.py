class MatDispDicc:
    def __init__(self, m, n, default=0, tipo='ren-col'):
        if tipo != "ren-col" and tipo != "col-ren":
            raise ValueError("Tipo inválido.")
        self.m = m
        self.n = n
        self.default = default
        self.tipo = tipo
        self.valores = {}
        self.max_len = 2
        self.colisiones = 0

    # Guarda datos en la matriz
    def guarda(self, i, j, valor):
        # Eliminamos lo que pudiera haber, si había algo, contamos la colisión
        if self.valores.get((i,j), None):
            self.colisiones += 1
        # Almacenamos
        if self.tipo == "ren-col":
            self.valores[(i, j)] = valor
        else:
            self.valores[(j, i)] = valor
        # Actualizamos máxima longitud de número (útil para la impresión)
        if len(str(valor)) > self.max_len:
            self.max_len = len(str(valor))
        
    # Recupera datos de la matriz
    def recupera(self, i, j):
        # Buscamos y devolvemos el dato o el default
        if self.tipo == "ren-col":
            key = (i,j)
        else:
            key = (j,i)
        return self.valores.get(key, self.default)
    
    # Operación de transposición
    def transpuesta(self):
        nuevaMat = MatDispDicc(self.n, self.m, self.default, self.tipo)
        nuevaMat.valores = {(j, i): v for (i, j), v in self.valores.items()} # Intercambiamos renglones por columnas
        nuevaMat.max_len = self.max_len
        return nuevaMat

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
    
    # Suma de matrices del tipo self + otra
    def suma(self, otra):
        # Checamos dimensiones
        if self.m != otra.m or self.n != otra.n:
            raise ValueError('Las matrices deben tener las mismas dimensiones para la suma.')
        # Creamos matriz donde almacenaremos la suma y copiamos datos de esta
        res = MatDispDicc(self.m, self.n, self.default, self.tipo)
        res.max_len = self.max_len
        res.valores = self.valores.copy()
        # Verificamos si tiene el mismo tipo y en base a eso tenemos el key
        if otra.tipo == self.tipo:
            # Iteramos sobre los datos guardados en la otra matriz
            for (i, j), v in otra.valores.items():
                if (i, j) in res.valores:    
                    res.valores[(i, j)] += v  # Si está en los valores de la original, lo sumamos
                else:
                    res.valores[(i, j)] = v   # Si no está, lo ponemos en la nueva
        else:
            # Iteramos sobre los datos guardados en la otra matriz
            for (j, i), v in otra.valores.items():
                if (i, j) in res.valores:    
                    res.valores[(i, j)] += v  # Si está en los valores de la original, lo sumamos
                else:
                    res.valores[(i, j)] = v   # Si no está, lo ponemos en la nueva
        return res
    
    # Multiplicación del tipo self * otra
    def multiplica(self, otra):
        if self.n != otra.m:
            raise ValueError('El número de col-rens de la primera matriz debe ser igual al número de filas de la segunda para la multiplicación.')
        res = MatDispDicc(self.m, otra.n, self.default, self.tipo)
        # Dividimos casos por tipos
        if self.tipo == "ren-col" and otra.tipo == self.tipo: # Ambos son ren-col
            for (i, k), v in self.valores.items():
                for j in range(otra.n):
                    if otra.recupera(k, j) != self.default:
                        key = (i, j)
                        if key in res.valores:
                            res.valores[key] += v * otra.recupera(k, j)
                        else:
                            res.valores[key] = v * otra.recupera(k, j)
        elif self.tipo=="ren-col": # Original es ren-col, otra es col-ren
            for (i, k), v in self.valores.items():
                for j in range(otra.n):
                    if otra.get(j, k) != self.default_value:
                        key = (i, j)
                        if key in res.valores:
                            res.valores[key] += v * otra.get(j, k)
                        else:
                            res.valores[key] = v * otra.get(j, k)
        elif self.tipo == otra.tipo: # Ambas son col-ren
            for (k, i), v in self.valores.items():
                for j in range(otra.n):
                    if otra.recupera(j, k) != self.default:
                        key = (j, i)
                        if key in res.valores:
                            res.valores[key] += v * otra.recupera(j, k)
                        else:
                            res.valores[key] = v * otra.recupera(j, k)
        else: # Original es col-ren, otra es ren-col
             for (k, i), v in self.valores.items():
                for j in range(otra.n):
                    if otra.recupera(k, j) != self.default:
                        key = (j, i)
                        if key in res.valores:
                            res.valores[key] += v * otra.recupera(k, j)
                        else:
                            res.valores[key] = v * otra.recupera(k, j)
        return res
    
from SkipListRemix import SkipList
import math

class MatDispSkL:
    def __init__(self, m, n, default=0):
        self.m = m
        self.n = n
        self.default = default
        maxNiv = int(math.log(m, 2))
        self.valores = SkipList(maxNiv, 0.5)
        self.max_len = 2
        self.colisiones = 0

    # Guarda datos en la matriz
    def guarda(self, i, j, valor):
        # Sumamos colisión
        if self.recupera(i, j) != self.default:
            self.colisiones += 1
        # Almacenamos
        ren = self.valores.buscar(i)
        if not ren:
            ren = self.valores.insertar(i)
        col = ren.lista.buscar(j)
        if not col:
            col = ren.lista.insertar(j)
        col.valor = valor
        # Actualizamos máxima longitud de número (útil para la impresión)
        if len(str(valor)) > self.max_len:
            self.max_len = len(str(valor))
        
    # Recupera datos de la matriz
    def recupera(self, i, j):
        res = self.default
        # Buscamos y devolvemos el dato o el default
        ren = self.valores.buscar(i)
        if ren:
            col = ren.lista.buscar(j)
            if col:
                res = col.valor
        return res
    
    # Operación de transposición
    def transpuesta(self):
        nuevaMat = MatDispSkL(self.n, self.m, self.default)
        nuevaSkl = SkipList(self.valores.max_level, self.valores.p)
        ren = self.valores.cabeza.siguiente[0]
        while ren:
            col = ren.lista.cabeza.siguiente[0]
            while col:
                nuevaSkl.insertar(col.indx, ren.indx, col.valor)
                col = col.siguiente[0]
            ren = ren.siguiente[0]
        nuevaMat.valores = nuevaSkl
        return nuevaMat

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

    # Suma a valor en cierta coordenada
    def sumaEn(self, i, j, valor):
        if self.recupera(i, j) == self.default:
            self.guarda(i, j, valor)
        else:
            ren = self.valores.buscar(i)
            col = ren.lista.buscar(j)
            col.valor += valor
    
    # Suma de matrices del tipo self + otra
    def suma(self, otra):
        # Checamos dimensiones
        if self.m != otra.m or self.n != otra.n:
            raise ValueError('Las matrices deben tener las mismas dimensiones para la suma.')
        # Creamos matriz donde almacenaremos la suma y copiamos datos de esta
        nuevaMat = MatDispSkL(self.n, self.m, self.default)
        nuevaSkl = nuevaMat.valores

        # Copiamos los datos de la propia
        ren = self.valores.cabeza.siguiente[0]
        while ren:
            col = ren.lista.cabeza.siguiente[0]
            while col:
                nuevaSkl.insertar(ren.indx, col.indx, col.valor)
                col = col.siguiente[0]
            ren = ren.siguiente[0]
        nuevaMat.valores = nuevaSkl
        
        renOtra = otra.valores.cabeza.siguiente[0]
        while renOtra:
            colOtra = renOtra.lista.cabeza.siguiente[0]
            while colOtra:
                nuevaMat.sumaEn(renOtra.indx, colOtra.indx, colOtra.valor)
                colOtra = colOtra.siguiente[0]
            renOtra = renOtra.siguiente[0]

        return nuevaMat
    
    

# =================================================================
import random, time

# Con esto probamos la inserción
def generaMatDispersaSkL(m, n, density, default=0, tipo='ren-col', imprim=False):
    mat = MatDispSkL(m, n, default)
    for k in range(int(m * n * density)):
        i = random.randint(0, m - 1)
        j = random.randint(0, n - 1)
        valor = random.randint(1, 10)
        if imprim: print("Insertando ", valor, " en ", str((i,j)))
        mat.guarda(i, j, valor)
    if imprim: print()
    return mat
    
# Prueba de programa
def evaluaMatDispSkL(M1, N1, default1, M2, N2, default2, sem, d1, d2, imprim=False):
    t0 = time.time()
    random.seed(sem)

    if imprim: print("Mat 1")
    mat1 = generaMatDispersaSkL(M1, N1, d1, default=default1, imprim=imprim)
    if imprim: print("Mat 2")
    mat2 = generaMatDispersaSkL(M2, N2, d2, tipo="col-ren", default=default2, imprim=imprim)

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
M1, N1 = 1, 1
M2, N2 = 1, 1
d1, d2 = 0.5, 0.5

# Llamamos el probador
evaluaMatDispSkL(M1, N1, 0, M2, N2, 0, sem, d1, d2, imprim=True)


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




# ==============================================


print("="*60)
print("Comparación dispersa vs densa \n")
for n in range(50, 251, 50):
    print("Comparación para matriz "+str(n)+"x"+str(n)+": ")
    tiempoDisp = evaluaMatDispDicc(n, n, 0, n, n, 0, random.random(), 0.75, 0.75)
    tiempoDens = evaluaMatDispSkL(n, n, 0, n, n, 0, random.random(), 0.75, 0.75)
    print("Tiempo de mat dispersa: ", tiempoDisp)
    print("Tiempo de mat densa: ", tiempoDens)
    print()
print("="*60)