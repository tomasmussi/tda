import sys
from grafo import Grafo


def llenar_grafo(grafo):
    with open('mapa.coords') as openfileobject:
        for line in openfileobject:
            vertices = line.split(' - ')
            v1 = vertices[0].rstrip()
            v2 = vertices[1].rstrip()
            grafo.agregarVertice(v1)
            grafo.agregarVertice(v2)
            grafo.agregarArista(v1, v2)

def main():
    if (len(sys.argv) != 7):
        raise Exception(
            'Debe ingresar las coordenadas x,y de los espias y del aeropuerto')
    spy1 = ' '.join([sys.argv[1], sys.argv[2]])
    spy2 = ' '.join([sys.argv[3], sys.argv[4]])
    aeropuerto = ' '.join([sys.argv[5], sys.argv[6]])
    
    print "El espia 1 esta en posicion " + spy1
    print "El espia 2 esta en posicion " + spy2
    print "El aeropuerto esta en posicion " + aeropuerto

    grafo = Grafo()

    llenar_grafo(grafo)
    
    print "espia 1 hasta aeropuerto " + str(grafo.distanciaMinima(spy1, aeropuerto))
    print "espia 2 hasta aeropuerto " + str(grafo.distanciaMinima(spy2, aeropuerto))


# TODO: Resolver...


if __name__ == '__main__':
    main()
