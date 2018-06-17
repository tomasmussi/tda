import sys
import copy
from grafo import Grafo
import operator

grafo = Grafo()

grafo.agregarVertice(0)
grafo.agregarVertice(2)
grafo.agregarVertice(3)
grafo.agregarVertice(1)


grafo.agregarArista(0,2,3)
grafo.agregarArista(2,1,3)
grafo.agregarArista(0,3,1)
grafo.agregarArista(3,1,2)

# Hago una copia del grafo original para despues comparar.
# original_net = copy.deepcopy(grafo)
original_net_plain = grafo.convertir_plano()
flujos = {}

for key in original_net_plain:
    net = copy.deepcopy(grafo)
    net.borrarArista(list(key)[0], list(key)[1])
    flujos[key] = net.ford_fulkerson(0, 1)

flujos = sorted(flujos.items(), key=operator.itemgetter(1))
most_important_edge, most_important_edge_maximum_flow = flujos[0][0], flujos[0][1]

print 'El flujo se vuelve minimo al sacar la arista: ' + str(most_important_edge) + ' dejando un flujo de ' + str(most_important_edge_maximum_flow)

grafo.borrarArista(most_important_edge[0], most_important_edge[1])

flujos = {}
original_net_plain = grafo.convertir_plano()
for key in original_net_plain:
    net = copy.deepcopy(grafo)
    net.borrarArista(list(key)[0], list(key)[1])
    flujos[key] = net.ford_fulkerson(0, 1)

flujos = sorted(flujos.items(), key=operator.itemgetter(1))
second_most_important_edge, second_most_important_edge_maximum_flow = flujos[0][0], flujos[0][1]

print 'El flujo se vuelve minimo al sacar la arista: ' + str(second_most_important_edge) + ' dejando un flujo de ' + str(second_most_important_edge_maximum_flow)


