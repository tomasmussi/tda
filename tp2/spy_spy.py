import sys
from grafo import Grafo

def llenarGrafo(grafo):
	with open('mapa.coords') as openfileobject:
			for line in openfileobject:
				vertices = line.split(' - ')
				v1 = vertices[0].rstrip()
				v2 = vertices[1].rstrip()
				grafo.agregarVertice(v1)
				grafo.agregarVertice(v2)
				grafo.agregarArista(v1, v2)
	print grafo.vertices

def main():
	if (len(sys.argv) != 7):
		raise Exception('Debe ingresar las coordenadas x,y de los espias y del aeropuerto')
	spy1 = (int(sys.argv[1]), int(sys.argv[2]))
	spy2 = (int(sys.argv[3]), int(sys.argv[4]))
	aeropuerto = (int(sys.argv[5]), int(sys.argv[6]))

	print "El espia 1 esta en posicion " + str(spy1)
	print "El espia 2 esta en posicion " + str(spy2)
	print "El aeropuerto esta en posicion " + str(aeropuerto)



	grafo = Grafo()
	llenarGrafo(grafo)


	# TODO: Resolver...


if __name__ == '__main__':
	main()