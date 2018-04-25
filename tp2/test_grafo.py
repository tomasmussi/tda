from grafo import Grafo

def construct_grafo_pesado():
	grafo = Grafo()
	grafo.agregarVertice('s')
	grafo.agregarVertice('A')
	grafo.agregarVertice('B')
	grafo.agregarVertice('C')
	grafo.agregarVertice('D')
	grafo.agregarVertice('t')

	grafo.agregarArista('s', 'A', 5)
	grafo.agregarArista('s', 'B', 2)

	grafo.agregarArista('A', 'C', 10)
	grafo.agregarArista('A', 'B', 3)

	grafo.agregarArista('B', 'C', 4)
	grafo.agregarArista('B', 'D', 1)

	grafo.agregarArista('C', 'D', 2)
	grafo.agregarArista('C', 't', 1)
	grafo.agregarArista('D', 't', 8)
	return grafo

def construct_grafo_no_pesado():
	grafo = Grafo()
	grafo.agregarVertice('s')
	grafo.agregarVertice('A')
	grafo.agregarVertice('B')
	grafo.agregarVertice('C')
	grafo.agregarVertice('D')
	grafo.agregarVertice('t')

	grafo.agregarArista('s', 'A')
	grafo.agregarArista('s', 'B')

	grafo.agregarArista('A', 'C')
	grafo.agregarArista('A', 'B')

	grafo.agregarArista('B', 'C')
	grafo.agregarArista('B', 'D')

	grafo.agregarArista('C', 'D')
	grafo.agregarArista('C', 't')
	grafo.agregarArista('D', 't')
	return grafo


def grafo_no_pesado_distancia_minima():
	# Construyo un grafo y pruebo los caminos de recorrido minimo
	grafo = construct_grafo_no_pesado()
	assert(grafo.distanciaMinima('s', 't') == 3)

def grafo_pesado_recorrido():
	grafo = construct_grafo_pesado()
	assert(grafo.recorridoMinimo('s', 't') == ['s', 'B', 'D', 'C', 't'])
	assert(grafo.distanciaMinima('s', 't') == 6)


def main():
	grafo_no_pesado_distancia_minima()
	grafo_pesado_recorrido()

if __name__ == '__main__':
	main()