import sys
import copy
from grafo import Grafo

grafo = Grafo()

grafo.agregarVertice(1)
grafo.agregarVertice(2)
grafo.agregarVertice(3)
grafo.agregarVertice(4)


grafo.agregarArista(1,2,3)
grafo.agregarArista(2,4,3)
grafo.agregarArista(1,3,1)
grafo.agregarArista(3,4,2)

# buscar maximo
for i in range(0,1):

    # Hago una copia del grafo original para despues comparar.
    grafo_viejo = copy.deepcopy(grafo)
    # Calculo ford fulkerson
    print "Flujo maximo" + str(grafo.ford_fulkerson(1,4))

    # Paso los grafos a una forma "plana", ej: grafo[1][2] = 3 <=> grafo[1,2] = 3
    grafo_viejo_plano = {}
    grafo_residual_plano = {}
    for key in grafo_viejo.vertices:
        for subkey in grafo_viejo.vertices[key]:
            grafo_viejo_plano[key, subkey] = grafo_viejo.vertices[key][subkey]

    for key in grafo.vertices:
        for subkey in grafo.vertices[key]:
            grafo_residual_plano[key, subkey] = grafo.vertices[key][subkey]
    
    # Calculo diferencia entre flujos
    diferencia_flujos = {x: grafo_viejo_plano[x] - grafo_residual_plano[x] for x in grafo_viejo_plano if x in grafo_residual_plano}
    max_diferencia = max([(value, key) for key, value in diferencia_flujos.items()])[1]
    print "Custodiar el" + str(max_diferencia)

    # Calculo otra copia para correr de nuevo el algoritmo.
    grafo = copy.deepcopy(grafo_viejo)
    grafo[max_diferencia(0)].pop(max_diferencia[1])
