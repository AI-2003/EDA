class MatDisp:

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


    def guarda(self, i, j, valor, tipo=None):

        # Verificamos casos con tipos no debidos
        if self.tipo != "ambos" and tipo: raise ValueError("No se debe indicar tipo, pues el de esta matriz está ya determinado.")
        if self.tipo == "ambos" and tipo != "ren-col" and tipo != "col-ren": raise ValueError("Tipo especificado inválido.")

        # Si ya está determinado el tipo de matriz, guardamos ese valor en tipo
        if not tipo:
            tipo = self.tipo

        # Almacenamos
        if tipo == "ren-col":
            self.valoresRenCol[(i, j)] = valor
            # Eliminamos en caso de que estuviera guardado en el formato contrario al que se caba de indicar
            self.valoresColRen.pop((j,i), None) # Indicamos un None por default para que no devuelva error si no encuentra nada
        else:
            self.valoresColRen[(j, i)] = valor
            self.valoresRenCol.pop((j, i), None)

        # Actualizamos máxima longitud de número (útil para la impresión)
        if len(str(valor)) > self.max_len:
            self.max_len = len(str(valor))

        

    def recupera(self, i, j):
        # Buscamos en ambos formatos. No nos importa el tipo, si no es el propio, ese dict estará vacío
        if (i,j) in self.valoresRenCol:
            return self.valoresRenCol[(i,j)]
        if (j, i) in self.valoresColRen:
            return self.valoresColRen[(j, i)]
        return self.default


    def transpuesta(self):
        nuevaMat = MatDisp(self.n, self.m, self.default, self.tipo)
        nuevaMat.valoresRenCol = {(j, i): v for (i, j), v in self.valoresRenCol.items()} # Intercambiamos renglones por columnas
        nuevaMat.valoresColRen = {(i, j): v for (j, i), v in self.valoresColRen.items()} # Intercambiamos columnas por renglones
        nuevaMat.max_len = self.max_len
        # Nota. Podríamos intercambias los diccionarios, pero habría varios subcasos. Por fines de simplicidad, se itera de esta manera
        return nuevaMat
    
    
    def impRen(self, i):

        # Iteramos sobre columnas
        print(f'{i:{self.max_len-1}}'+"|", end=' ')
        for j in range(self.n):
            print(f'{self.recupera(i, j):{self.max_len}}', end=' ')    # Longitud estandarizada


    def impCol(self, j):

        # Iteramos sobre renglones
        print("\u0332".join(f'{j:{self.max_len}}'))
        for i in range(self.n):
            print(f'{self.recupera(i, j):{self.max_len}}', end='\n')    # Longitud estandarizada


    def impMat(self):

        # Iteramos sobre renglones
        print("\u0332".join(f'{"i|":{self.max_len}}'), end=' ')
        for k in [f'{i:{self.max_len}}' for i in range(self.n)]: print("\u0332".join(k), end=' ')
        print()
        for i in range(self.m):
            self.impRen(i)     # Imprimimos cada renglón
            print()


    def suma(self, otra):

        # Checamos dimensiones
        if self.m != otra.m or self.n != otra.n:
            raise ValueError('Las matrices deben tener las mismas dimensiones para la suma.')
        
        # Creamos matriz donde almacenaremos la suma y copiamos datos de esta
        res = MatDisp(self.m, self.n, self.default, self.tipo)
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
    
    
    # Multiplicación del tipo self * otra
    def multiplica(self, otra):

        # Verificamos dimensiones
        if self.n != otra.m:
            raise ValueError('El número de col-rens de la primera matriz debe ser igual al número de filas de la segunda para la multiplicación.')
        
        # Creamos matriz donde almacenaremos la multiplicación
        res = MatDisp(self.m, self.n, self.default, self.tipo)
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
                    elif key in res.valoresColRen:      # Se agrega este caso a diferencia del ciclo ren-col, pues ahí era imposible que existiera
                        res.valoresColRen[key] += val
                    else:
                        res.valoresColRen[key] = val

                    # Actualizamos la len
                    if res.max_len < len(str(val)):
                        res.max_len = len(str(val))
        return res
        


# ====================================
# Prueba
# ====================================

import random


# Con esto probamos la inserción
def generaMatDispersa(m, n, density, default=0, tipo='ren-col'):
    mat = MatDisp(m, n, default, tipo)
    for k in range(int(m * n * density)):
        i = random.randint(0, m - 1)
        j = random.randint(0, n - 1)
        valor = random.randint(1, 10)
        print("Insertando ", valor, " en ", str((i,j)))
        mat.guarda(i, j, valor)
    print()
    return mat



if __name__ == "__main__":
    
    # Establecemos la semilla para la reproducibilidad
    sem = 1001
    random.seed(sem)

    # Generamos las matrices dispersas
    M1, N1 = 10, 10
    M2, N2 = 10, 10
    d1, d2 = 0.075, 0.075
    print("Mat 1")
    mat1 = generaMatDispersa(M1, N1, d1)
    print("Mat 2")
    mat2 = generaMatDispersa(M2, N2, d2, tipo="col-ren")

    # Imprimimos las matrices generadas
    print("Matriz 1:")
    mat1.impMat()
    print("\nMatriz 2:")
    mat2.impMat()

    # Prueba del método de recuperación
    print(f"\nRecuperamos el elemento en la posición (0,0) de la Matriz 1: {mat1.recupera(0, 0)}")
    print(f"Recuperamos el elemento en la posición (6,5) de la Matriz 1: {mat1.recupera(6, 5)}")

    # Prueba del método de transposición
    print(f"\nTranspuesta de la Matriz 2:")
    mat2_transpuesta = mat2.transpuesta()
    mat2_transpuesta.impMat()

    # Prueba de los métodos de suma y multiplicación
    print("\nSuma de las matrices 1 y 2:")
    matriz_suma = mat1.suma(mat2)
    matriz_suma.impMat()

    print("\nProducto de mat 1 * mat 2:")
    matriz_producto = mat1.multiplica(mat2)
    matriz_producto.impMat()

    renglon, columna = 6, 5
    print(f"\nImpresión del renglón {renglon} de la Matriz 1:")
    mat1.impRen(renglon)
    print()
    print(f"\nImpresión de la columna {columna} de la Matriz 1:")
    mat1.impCol(columna)
