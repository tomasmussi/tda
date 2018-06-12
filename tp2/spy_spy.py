import sys
from grafo import Grafo
from scipy.spatial import distance


def llenar_grafo(grafo, con_distancias = False):
    with open('mapa.coords') as openfileobject:
        for line in openfileobject:
            vertices = line.split(' - ')
            v1 = vertices[0].rstrip()
            v2 = vertices[1].rstrip()
            grafo.agregarVertice(v1)
            grafo.agregarVertice(v2)
            distancia = 1
            if con_distancias:
                v1_coord = tuple(map(int, v1.split(' ')))
                v2_coord = tuple(map(int, v2.split(' ')))
                distancia = distance.euclidean(v1_coord, v2_coord)
            grafo.agregarArista(v1, v2, distancia)

def obtener_camino_bfs(nodos, destino):
    camino = [destino]
    vertice_actual = destino
    while nodos[vertice_actual] != None and nodos[vertice_actual] != vertice_actual:
        camino.append(nodos[vertice_actual])
        vertice_actual = nodos[vertice_actual]
    return camino

def main():
    # if (len(sys.argv) != 7):
    #     raise Exception(
    #         'Debe ingresar las coordenadas x,y de los espias y del aeropuerto')
    spy1 = '1 2'
    spy2 = '3 4'
    aeropuerto = '5 6'

    # print "El espia 1 esta en posicion " + spy1
    # print "El espia 2 esta en posicion " + spy2
    # print "El aeropuerto esta en posicion " + aeropuerto + "\n"

    grafo = Grafo()
    grafo_con_distancias = Grafo()

    llenar_grafo(grafo)
    len(grafo.vertices.keys)
    llenar_grafo(grafo_con_distancias, True)

    # Punto 1
    nodos, distancias = grafo.bfs(aeropuerto)
    print "1) Resultado sin pesos en las aristas:"
    print "Distancia espia 1 hasta aeropuerto: " + str(distancias[spy1])
    print "Distancia espia 2 hasta aeropuerto: " + str(distancias[spy2])
    print "Gana espia 1" if distancias[spy1] < distancias[spy2] else "Gana espia 2"
    print "\n"
    # Punto 2
    print "2) Resultado con pesos en las aristas:"
    print "espia 1 hasta aeropuerto " + str(grafo_con_distancias.distanciaMinima(spy1, aeropuerto))
    print "espia 2 hasta aeropuerto " + str(grafo_con_distancias.distanciaMinima(spy2, aeropuerto))
    print "\n"
    # Punto 4
    # sin pesos
    print "4)"
    print "4)a) camino minimo sin pesos es:"
    print "espia 1 hasta aeropuerto " + ', '.join(obtener_camino_bfs(nodos, spy1))
    print "espia 2 hasta aeropuerto " + ', '.join(obtener_camino_bfs(nodos, spy2))
    print "\n"
    # con pesos
    print "4)b) camino minimo con pesos es:"
    print "espia 1 hasta aeropuerto " + str(grafo_con_distancias.recorridoMinimo(spy1, aeropuerto))
    print "espia 2 hasta aeropuerto " + str(grafo_con_distancias.recorridoMinimo(spy2, aeropuerto))


if __name__ == '__main__':
    main()
