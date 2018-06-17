import sys
import copy
from grafo import Grafo
import operator

grafo = Grafo()

grafo.agregarVertice(1)
grafo.agregarVertice(2)
grafo.agregarVertice(3)
grafo.agregarVertice(4)


grafo.agregarArista(1,2,3)
grafo.agregarArista(2,4,3)
grafo.agregarArista(1,3,1)
grafo.agregarArista(3,4,2)

# Hago una copia del grafo original para despues comparar.
grafo_viejo = copy.deepcopy(grafo)
# Calculo ford fulkerson
print "Flujo maximo" + str(grafo.ford_fulkerson(1,4))

# Paso los grafos a una forma "plana", ej: grafo[1][2] = 3 <=> grafo[1,2] = 3

# Agrega complejidad 2M = cantidad de aristas mas dos veces para analizar el grafo de forma mas "amigable"
grafo_viejo_plano = grafo_viejo.convertir_plano()
grafo_residual_plano = grafo.convertir_plano()

# Calculo diferencia entre flujos
diferencia_flujos = {x: grafo_viejo_plano[x] - grafo_residual_plano[x] for x in grafo_viejo_plano if x in grafo_residual_plano}
# Ordeno las diferencias
diferencia_flujos = sorted(diferencia_flujos.items(), key=operator.itemgetter(1))

print "Custodiar el: " + str(diferencia_flujos[-1][0]) + ' que lleva un flujo de ' + str(diferencia_flujos[-1][1]) + \
     ' y el: ' + str(diferencia_flujos[-2][0]) + ' que lleva un flujo de ' +  str(diferencia_flujos[-2][1])
