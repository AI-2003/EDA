import Network as biblio

print("OK")

et = biblio.EstructuraTopo()
et.agrega('a','b')
et.agrega('a','c')
et.agrega('b','d')
et.agrega('c','e')
et.agrega('d','f')
et.agrega('e','f')
et.agrega('f','g')
et.agrega('f','h')
et.agrega('g','i')
et.agrega('h','j')
et.agrega('i','j')
et.agrega('j','k')
et.ordenaT()
print(et)