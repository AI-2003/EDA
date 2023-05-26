import random, math, time
from SkipList_Bing_02 import SkipList


# =================================
#  Utilería
# ================================= 
def intersection(list_a, list_b):
    return [ e for e in list_a if e in list_b ]       

# =================================
#  Evaluadores
# ================================= 

def evaluaSkip(n, p, I, sem=random.random(), imprime=False):
    res = []

    max = int(math.log(n,2))+1
    sl = SkipList(max, p)
    random.seed(sem)

    if imprime:
        print("Semilla: ", sem, "\n")

    # Elementos a insertar
    elemsIns = []
    for i in range(n):
        elemsIns.append( int(I[0] + random.random()*(I[1]-I[0])) )
    # Elementos a buscar
    elemsBus = []
    for i in range(n):
        elemsBus.append( int(I[0] + random.random()*(I[1]-I[0])) )
    # Elementos a eliminar
    elemsEl = []
    for i in range(n):
        elemsEl.append( int(I[0] + random.random()*(I[1]-I[0])) )

    # Ciclo de insertación
    t0 = time.time()
    for elem in elemsIns:
        sl.insertar(elem)
    t1 = time.time()
    res.append(t1-t0)
    if imprime:
        print("Elementos insertados: ", elemsIns)
        print(sl.imp())


    # Ciclo de búsqueda
    t0 = time.time()
    for elem in elemsBus:
        sl.buscar(elem)
    t1 = time.time()
    res.append(t1-t0)


    # Ciclo de eliminación
    t0 = time.time()
    for elem in elemsEl:
        sl.eliminar(elem)
    t1 = time.time()
    res.append(t1-t0)
    if imprime:
        print("LLamados a eliminar: ", elemsEl)
        eliminados = list(dict.fromkeys(intersection(elemsIns, elemsEl)))
        eliminados.sort()
        print("Eliminados: ", eliminados)
        print(sl.imp())

    return res

def evaluaDict(n, p, I, sem=random.random(), imprime=False):
    res = []
    dict = {}
    random.seed(sem)

    if imprime:
        print("Semilla: ", sem, "\n")

    # Elementos a insertar
    elemsIns = []
    for i in range(n):
        elemsIns.append( int(I[0] + random.random()*(I[1]-I[0])) )
    # Elementos a buscar
    elemsBus = []
    for i in range(n):
        elemsBus.append( int(I[0] + random.random()*(I[1]-I[0])) )
    # Elementos a eliminar
    elemsEl = []
    for i in range(n):
        elemsEl.append( int(I[0] + random.random()*(I[1]-I[0])) )

    # Ciclo de insertación
    t0 = time.time()
    for elem in elemsIns:
        dict[elem] = elem
    t1 = time.time()
    res.append(t1-t0)
    if imprime:
        print("Elementos insertados: ", elemsIns)
        print(dict)

    # Ciclo de búsqueda
    t0 = time.time()
    for elem in elemsBus:
        dict.get(elem, None)
    t1 = time.time()
    res.append(t1-t0)

    # Ciclo de eliminación
    t0 = time.time()
    for elem in elemsEl:
        dict.pop(elem, None)
    t1 = time.time()
    res.append(t1-t0)
    if imprime:
        print("LLamados a eliminar: ", elemsEl)
        eliminados = list(dict.fromkeys(intersection(elemsIns, elemsEl)))
        eliminados.sort()
        print("Eliminados: ", eliminados)
        print(dict)

    return res




print("="*60)

print("\nFormato: [Tiempo de inserción, tiempo de búsqueda, tiempo de eliminación]\n")
for expon in range(6):
    n = 10**expon
    I = (0,n*10)
    sem = random.random()

    print("Para ", n, "elementos con valor dentro de ", I)

    skipT = evaluaSkip(n, 0.5, I, sem)
    dictT = evaluaDict(n, 0.5, I, sem)

    print("Skip: ", skipT, "Total: ", sum(skipT))
    print("Dict: ", dictT, "Total: ", sum(dictT))
    print("")

print("="*60)