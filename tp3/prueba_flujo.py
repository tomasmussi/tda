import sys
import copy
from grafo import Grafo

grafo = Grafo()

grafo.agregarVertice(1)
grafo.agregarVertice(2)
grafo.agregarVertice(3)
grafo.agregarVertice(4)


grafo.agregarArista(1,2,1)
grafo.agregarArista(2,4,3)
grafo.agregarArista(1,3,1)
grafo.agregarArista(3,4,1)


grafo_viejo = copy.deepcopy(grafo)

print str(grafo.ford_fulkerson(1,4))

print 'gilada'